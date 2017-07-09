#!/usr/bin/python3

"""
Engine used for processing test plans.
"""

from __future__ import print_function
import os
import sys
import shutil
import subprocess
import socket
import signal
from time import sleep
from threading import Thread
import multiprocessing
import zmq

sys.path.append('/home/smith/Dropbox/')
from ellida.manager.ellida_manager import EllidaManager
from ellida.settings import EllidaSettings

class EllidaEngine(multiprocessing.Process):
    """ Ellida engine. Builds scripts that run the tests.
    """
    build_path = "build/"
    build_handlers = []
    poky_build = "/home/smith/projects/poky/build/"
    # local_addr = "192.168.7.1"
    # target_addr = "192.168.7.2"
    target_addr = "192.168.7.2"
    local_addr = "192.168.10.4"

    comm_port = 9778
    log_port = 9779
    shutdown = False
    conf_path = "../res/ellida.conf" # make this non-relative <<<<<<<<<<<<<<<<<<<<<
    test_sets = ["test_set1", "test_set2"]

    def __init__(self):
        self.manager = EllidaManager()
        self.supported_specs = self.manager.get_specs()
        self.config = {}
        self.active_threads = []
        self.active_sockets = []
        self.__setup()
        self.__network_setup()
        print("Ellida engine initialized.")

    def __network_setup(self):
        self.context = zmq.Context()
        self.engine_socket = self.context.socket(zmq.REP)
        self.engine_socket.bind("tcp://*:%s" % EllidaSettings.ENGINE_SOCKET)

    def __setup(self):
        # self.__read_config()
        os.makedirs(self.build_path, exist_ok=True)
        for spec in self.supported_specs:
            self.build_handlers.append(open(self.build_path + str(spec) +
                                            ".sh", "w+"))

    def __read_config(self):
        with open(self.conf_path) as conf_file:
            current_config = conf_file.readlines()
        for setting in current_config: # check for wrong format like: /home/smith = CONF_FILE
            params = setting.split('=')
            if len(params) > 1:
                self.config[params[0].strip()] = params[1].strip()
            else:
                raise EllidaEngineError("\
                    Wrong file format, you can find an example in the res/ directory.")
        self.target_addr = self.config['TARGET_ADDR']
        self.local_addr = self.config['LOCAL_ADDR']
        print("Config loaded: ", self.config)

    @classmethod
    def build_ltp(cls):
        pass

    @classmethod
    def __direct_imagetest_build(cls, tests):
        """
        Make the necessary setup for image tests without an auxiliary bash script.
        """
        # The path must be taken from somwhere else <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        conf_path = "/home/smith/projects/poky/build/conf/local.conf"
        backup_path = "../res/local.conf"
        test_destination_path = "/home/smith/projects/poky/meta/lib/oeqa/runtime/"
        test_source_path = "../database/tests/"
        # backup the loca.conf
        shutil.copy(conf_path, backup_path) # generate this command dinamically
        comm = ["sudo",
                "/home/smith/projects/poky/scripts/runqemu-gen-tapdevs",
                "1000", "1000", "1",
                "/home/smith/projects/poky/build/tmp/sysroots/x86_64-linux"]
        proc = subprocess.Popen(comm,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        print("Tapgen resut: ", proc.communicate())
        conf_handle = open(conf_path, 'r+')
        conf_data = conf_handle.readlines()
        if 'INHERIT += "testimage\n"' not in conf_data or not "INHERIT += 'testimage'\n":
            conf_data.append('\nINHERIT += "testimage"\n')
        flag = False
        for i in range(len(conf_data)):
            if "TEST_SUITES" in conf_data[i]:
                conf_data[i] = "\nTEST_SUITES = \"" + " ".join(tests) + "\"\n"
                flag = True
                break
        if not flag:
            conf_data.append("\nTEST_SUITES = \"" + " ".join(tests) + "\"\n")
        print("\nTEST_SUITES = \"" + " ".join(tests) + "\"")
        conf_handle.seek(0) ## very inefficient, do it better <<<<<<<<<<<<
        conf_handle.write("".join(conf_data))
        for test in tests:
            # print("copy: ", test_source_path + test + ".py", test_destination_path + test + ".py")
            shutil.copy2(test_source_path + test + ".py", test_destination_path + test + ".py")
        conf_handle.close()

    @classmethod
    def build_imagetest(cls, tests):
        """
        1. Setup tap device
        id $USER
        sudo /home/smith/projects/poky/scripts/runqemu-gen-tapdevs <uid> <gid> <num> <native-sysroot-basedir>
        2. add INHERIT += "testimage" in local.conf
        3. add TEST_SUITES = test_list in local.conf
        4. copy tests in meta/lib/oeqa/runtime
        5. call bitbake core-image-minimal -c testimage
        """
        conf_path = "/home/smith/projects/poky/build/conf/local.conf"
        imagetest_script_path = "imagetest_script.sh"
        test_string = "\"" + " ".join(tests) + "\""
        imagetest_script = """
sudo /home/smith/projects/poky/scripts/runqemu-gen-tapdevs 1000 1000 1 /home/smith/projects/poky/build/tmp/sysroots/x86_64-linux
grep -q -F 'INHERIT += "testimage"' """ + conf_path + """ || (echo '' >> """ + conf_path + """ && echo 'INHERIT += "testimage"' >> """ + conf_path + """)
if grep -q -F 'TEST_SUITES' """ + conf_path + """
then
    sed -i 's/.*TEST_SUITES.*/TEST_SUITES = """ + test_string + """/' """ + conf_path + """
else
    echo 'TEST_SUITES = """ + test_string + """' >> """ + conf_path + """
fi
"""
        with open(imagetest_script_path, 'w+') as imagetest_script_handle:
            imagetest_script_handle.write(imagetest_script)
        os.chmod(imagetest_script_path, 0o755)


    def __log_interpreter(self, log_socket):
        print("Started log interpreter thread")
        while not self.shutdown:
            try:
                packet, _ = log_socket.recvfrom(1024)
                packet = packet.decode('utf-8')
                if packet:
                    print("Received: ", packet)
                else:
                    break
            except socket.error:
                pass

    def signal_handler(self, signal, frame):
        print("Engine shuting down")
        self.shutdown = True
        self.close_engine()
        sys.exit(0)

    # implement a good producer-consumer the sender should consume sets of tests, the manager should add more sets <<<<<<<<<<<<<<<<<<<<<<<<<<
    def __command_sender(self, comm_socket):
        print("Connecting to daemon on ", self.target_addr, "...")
        while not self.shutdown:
            try:
                comm_socket.connect((self.target_addr, self.comm_port))
                break
            except socket.error:
                sleep(1)
        print("Connected to daemon.")
        for test_set in self.test_sets:
            payload = bytes(test_set, 'utf-8')
            ret = comm_socket.sendto(payload, (self.target_addr, self.comm_port))
            print("Sent command: ", test_set, " [", ret, "]")

    def start_engine(self):
        """
        1. Folosesc managerul ca sa parsez specificatia
        2. Iau arborele de dependinte si il parcurg
        3. Generez scripturi de configurare si rulare pentru Image Tests.
        """
        print("Engine running")
        signal.signal(signal.SIGINT, self.signal_handler)

        (self.spec_database, self.spec_graphs) = self.manager.parse_specifications()

        spec = 'cgl'
        test_sets = {}
        test_sets[spec] = []
        requirements = self.manager.get_requirements(spec)
        for req in requirements:
            for x in self.spec_database[spec]: # change this <<<<<<<<<<<<
                if x['id'] == req:
                    if x['tests']:
                        test_sets[spec].append(x['tests'])
                    break
        tests = []
        for x in test_sets[spec]:
            for y in x:
                if len(y['name']) > 2 and y['name'] != 'empty':
                    tests.append(y['name'])
        print("Tests to be run for", spec, ":", set(tests))
        self.build_imagetest(set(tests))

        command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        command_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        command_socket.bind((self.local_addr, self.comm_port))
        sender_thread = Thread(target=self.__command_sender, args=(command_socket,))
        sender_thread.daemon = True
        sender_thread.start()

        log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        log_socket.bind((self.local_addr, self.log_port))
        log_socket.listen()

        while not self.shutdown:
            print("Engine waiting for loggers...")
            (active_socket, address) = log_socket.accept()
            print("Accepted logger from ", address)
            log_thread = Thread(target=self.__log_interpreter, args=(active_socket,))
            log_thread.daemon = True
            log_thread.start()
            self.active_threads.append(log_thread)
            self.active_sockets.append(active_socket)

        for thr in self.active_threads:
            thr.join()
        sender_thread.join()
        for sock in self.active_sockets:
            sock.close()
        log_socket.close()
        command_socket.close()

    def close_engine(self):
        """ Do cleanup.
        """
        for handle in self.build_handlers:
            handle.close()
        shutil.rmtree(self.build_path)

    def install_providers(self):
        providers = self.manager.get_providers()

    def __setup_image_tests(self):
        """
        1. copy scripts
        2. add list of scripts to file
        """
        pass

    def shutdown(self):
        self.exit.set()

def main():
    """ Main function.
    """
    engine = EllidaEngine()
    engine.start_engine()


if __name__ == '__main__':
    main()

class EllidaEngineError(Exception):
    def __init__(self, message = "Ellida engine error"):
        self.message = "\033[91[E] " + message + "\e[0m"
