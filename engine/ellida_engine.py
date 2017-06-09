#!/usr/bin/python3

"""
Engine used for processing test plans.
Next todo:

[] Generate dummy running scripts for LTP and image tests.
    [] Setup Image Tests: copy tests in the right directory, config file with
    the list of tests
[] Should support:
    [] Selenium
    [] LTTng
    [] perf
    [] systemtap -> cum controlez sau inserez module de kernel?
"""

import sys
sys.path.append('/home/smith/Dropbox/')
import os
import shutil
import subprocess
from ellida.manager.ellida_manager import EllidaManager

class EllidaEngine(object):
    """ Ellida engine. Builds scripts that run the tests.
    """
    build_path = "build/"
    build_handlers = []
    poky_build = "/home/smith/projects/poky/build/"

    def __init__(self):
        self.manager = EllidaManager()
        self.supported_specs = self.manager.get_specs()
        self.__setup()
        print("Ellida engine initialized.")

    def __setup(self):
        os.makedirs(self.build_path, exist_ok=True)
        for spec in self.supported_specs:
            self.build_handlers.append(open(self.build_path + str(spec) +
                                            ".sh", "w+"))

    @classmethod
    def build_ltp(cls):
        pass

    def __direct_imagetest_build(self, tests):
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
        comm = ["sudo", "/home/smith/projects/poky/scripts/runqemu-gen-tapdevs", "1000", "1000", "1", "/home/smith/projects/poky/build/tmp/sysroots/x86_64-linux"]
        proc = subprocess.Popen(comm, shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        print("Tapgen resut: ", proc.communicate())
        conf_handle  = open(conf_path, 'r+')
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
        conf_handle.seek(0) ## very inefficient, do it better <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        conf_handle.write("".join(conf_data))
        for test in tests:
            # print("copy: ", test_source_path + test + ".py", test_destination_path + test + ".py")
            shutil.copy2(test_source_path + test + ".py", test_destination_path + test + ".py")
        conf_handle.close()

    def build_imagetest(self, tests):
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


    def start_engine(self):
        """
        1. Folosesc managerul ca sa parsez specificatia
        2. Iau arborele de dependinte si il parcurg
        3. Generez scripturi de configurare si rulare pentru Image Tests.
        """
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

    def close_engine(self):
        """ Do cleanup.
        """
        for handle in self.build_handlers:
            handle.close()
        shutil.rmtree(self.build_path)

    def __setup_image_tests(self):
        """
        1. copy scripts
        2. add list of scripts to file
        """
        pass


def main():
    """ Main function.
    """
    engine = EllidaEngine()
    engine.start_engine()

if __name__ == '__main__':
    main()

class EllidaEngineError(Exception):
    def __init__(self, message = "Ellida engine error"):
        self.message = "[E] " + message