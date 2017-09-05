#!/usr/bin/python3

"""
Object used to define and create a daemon process on the guest machine that is subjected to testing.
The daemon is responsible for receiving a test plan, executing it and returning the results.
"""

from __future__ import print_function

import socket
import logging
import signal
import sys
import time
import zmq
import json
from threading import Thread

sys.path.append('/usr/bin/python3.5/site-packages/')
sys.path.append('/usr/bin/python2.7/site-packages/')
sys.path.append('/home/smith/Dropbox/')
sys.path.append('../../')


from daemonize import Daemonize

# from ellidadaemon.settings import EllidaSettings
# from ellidadaemon.providers.provider import Provider
# from ellidadaemon.providers.ltp_provider import LtpProvider
# from ellidadaemon.providers.core_provider import CoreProvider

from ellida.providers.provider import Provider
from ellida.providers.ltp_provider import LtpProvider
from ellida.providers.core_provider import CoreProvider
from ellida.settings import EllidaSettings

class EllidaDaemon(object):
    """
    Daemon object that runs on target machine and manages communication between
    Ellida engine and the target
    """
    shutdown = False
    _PROC_PID = "../res/ellida.pid"
    _RECV_TIMEOUT = 1000
    _TARGET_ROOT = "/opt/ellida_tests/"

    def __init__(self):
        self.__log_setup()
        self.active_threads = []
        self.active_sockets = []
        self.__sockets = []
        # self.__network_setup()

    def __network_setup(self):
        print("Daemon setup done")
        self.__context = zmq.Context()
        self.__poller = zmq.Poller()
        self.__engine_socket = self.__context.socket(zmq.PAIR)
        self.__engine_socket.connect("tcp://" + EllidaSettings.ENGINE_ADDR + ":" +
                                   str(EllidaSettings.DAEMON_SOCKET))
        self.__poller.register(self.__engine_socket, zmq.POLLIN)

    def kill_handler(self, signal, frame):
        self.logger.debug("Ellida daemon shuting down")
        self.shutdown = True
        self.__engine_unregister()
        for sock in self.__sockets:
            sock.close()
        sys.exit(0)

    def __log_setup(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        fh = logging.FileHandler("/tmp/test.log", "a+")
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        self.log_fds = [fh.stream.fileno()]
        self.logger.debug("Logger setup finished")

    def __log_sender(self, log_socket):
        self.logger.debug("Connecting to daemon on " + self.engine_addr + "...")
        while not self.shutdown:
            try:
                log_socket.connect((self.engine_addr, self.log_port))
                break
            except socket.error:
                time.sleep(1)
        for log in self.log_results:
            payload = bytes(log, 'utf-8')
            log_socket.sendto(payload, (self.engine_addr, self.log_port))

    def __command_interpreter(self, command_socket):
        print("Started log interpreter thread")
        while not self.shutdown:
            try:
                packet, _ = command_socket.recvfrom(1024)
                packet = packet.decode('utf-8')
                if packet:
                    print("Received: ", packet, len(packet))
                else:
                    break
            except socket.error:
                pass

    def __execute_test(self, target):
        metadata_path = self._TARGET_ROOT + target[1][2:] + '/' + target[0] + '/' + target[0] + '.json'
        with open(metadata_path) as metadata_file:
            metadata = json.load(metadata_file)
        print("Loaded:", metadata)
        res = None
        if metadata['provider'] == "ltp":
            provider = LtpProvider()
        elif metadata['provider'] == "core":
            provider = CoreProvider()
        else:
            raise ValueError
        test_info = target[1][2:].split('/')
        provider.configure({'spec': test_info[0], 'req': test_info[1], 'set': target[0]})
        for x in range(len(metadata['targets'])):
            metadata['targets'][x] = self._TARGET_ROOT + target[1][2:] + '/' + target[0] + '/' + metadata['targets'][x]
        print("sending targets:", metadata['targets'])
        result = provider.execute(metadata['targets'])
        provider.cleanup()
        return result

    def __engine_register(self):
        self.__engine_socket.send_string("init_1")

    def __engine_unregister(self):
        self.__engine_socket.send_string("exit_1")

    """ Ideas:
    Try to make multiple comunication modes based on the zmq architecture in order to provide
    parallel testing. Several machines running in parallel could connect to the same engine and run
    different parts of the testing suite.
    Call it EllidaGrid.
    """
    def __daemon_thread(self):
        # self.__context = zmq.Context()
        # self.__engine_socket = self.__context.socket(zmq.PAIR)
        # self.__engine_socket.connect("tcp://" + EllidaSettings.ENGINE_ADDR + ":" +
        #                            str(EllidaSettings.DAEMON_SOCKET))
        self.__network_setup()
        self.__engine_register()
        while not self.shutdown:
            sockets = dict(self.__poller.poll(self._RECV_TIMEOUT))
            if sockets.get(self.__engine_socket) == zmq.POLLIN:
                packet = self.__engine_socket.recv_json()
                sys.stdout.write("[D] received: " + str(packet) + '\n')
                sys.stdout.flush()
                if packet['event'] == "req_exe":
                    if 'addr' not in packet or 'port' not in packet:
                        print(Fore.RED + "No information about the connection for request:", packet)
                        sys.exit(1)
                    fsock = self.__context.socket(zmq.PAIR)
                    self.__sockets.append(fsock)
                    fsock.connect("tcp://" + packet['addr'] + ':' + packet['port'])
                    for test in packet['value']:
                        print('Executing: ', test)
                        results = self.__execute_test(eval(test))
                        for result in results:
                            fsock.send(result)
                    fsock.send(bytes("ELLIDA_EXIT", 'utf-8'))
                    fsock.close()
            else:
                # self.__engine_socket.send_string(EllidaSettings.random_hello())
                time.sleep(5)

        print("Daemon thread terminated")

    def start_daemon(self):
        """ TODO """
        self.logger.debug("Starting the daemon")
        signal.signal(signal.SIGINT, self.kill_handler)
        self.__daemon_thread()
        print("Main daemon thread finish")

def main():
    ellida_daemon = EllidaDaemon()
    ellida_daemon.start_daemon()

if __name__ == '__main__':
    main()
