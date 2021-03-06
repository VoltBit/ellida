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
from time import sleep
from threading import Thread
import zmq
import json

sys.path.append('/usr/bin/python3.5/site-packages/')
sys.path.append('/usr/bin/python2.7/site-packages/')
sys.path.append('/home/smith/Dropbox/')


from daemonize import Daemonize

from ellida.providers.provider import Provider
from ellida.providers.ltp_provider import LtpProvider
from ellida.settings import EllidaSettings

class EllidaDaemon(object):
    """
    Daemon object that runs on target machine and manages communication between
    Ellida engine and the target
    """
    proc_pid = "../res/ellida.pid"
    shutdown = False
    RECV_TIMEOUT = 1000

    def __init__(self):
        self.__log_setup()
        self.active_threads = []
        self.active_sockets = []
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
        """ TODO """
        self.logger.debug("Ellida daemon shuting down")
        self.shutdown = True
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

    def __execute_test(self, meta_test):
        # test_info = meta_test.split('.')
        res = None
        if meta_test == 'testing':
            provider = LtpProvider()
            provider.configure({'spec': "agl", 'req': '711', 'set': 2})
            provider.execute(["agl/services/AGL.711/set_2/ltp_control_file"])
            res = provider.get_raw_result()
            print("Result: " + str(res))
            sleep(1)
            res = provider.get_raw_result()
            print("Result: " + str(res))
            sleep(2)
            provider.cleanup()
        print("Result: " + str(res))


    def __daemon_thread(self):
        self.__network_setup()
        while not self.shutdown:
            sockets = dict(self.__poller.poll(self.RECV_TIMEOUT))
            if sockets.get(self.__engine_socket) == zmq.POLLIN:
                packet = self.__engine_socket.recv_json()
                # print("[D] received: ", packet)
                sys.stdout.write("[D] received: " + str(packet) + '\n')
                sys.stdout.flush()
                if packet['event'] == "req_exe":
                    self.__execute_test(packet['value'])
            else:
                self.__engine_socket.send_string(EllidaSettings.random_hello())
                sleep(1)

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
