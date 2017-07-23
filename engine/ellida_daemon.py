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

from daemonize import Daemonize
# from providers import LtpProvider
# from settings import EllidaSettings
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


    def __init__(self):
        self.__log_setup()
        self.active_threads = []
        self.active_sockets = []
        # self.__network_setup()

    def __network_setup(self):
        print("Daemon setup done")
        self.__context = zmq.Context()
        self.__engine_socket = self.__context.socket(zmq.PAIR)
        self.__engine_socket.connect("tcp://" + EllidaSettings.ENGINE_ADDR + ":" +
                                   str(EllidaSettings.DAEMON_SOCKET))

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

    def __log_sender(self, log_socket):
        self.logger.debug("Connecting to daemon on " + self.engine_addr + "...")
        while not self.shutdown:
            try:
                log_socket.connect((self.engine_addr, self.log_port))
                break
            except socket.error:
                sleep(1)
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

    def __daemon_thread_old(self):
        # start log sender thread
        self.logger.debug("Daemon running")
        log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        log_socket.bind((self.local_addr, self.log_port))
        log_thread = Thread(target=self.__log_sender, args=(log_socket,))
        log_thread.daemon = True
        log_thread.start()

        self.logger.debug("Daemon test")
        # start command listener
        command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        command_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        command_socket.bind((self.local_addr, self.comm_port))
        command_socket.listen(0)
        while not self.shutdown:
            self.logger.debug("Daemon waiting for commands...")
            (active_socket, address) = command_socket.accept()
            self.active_sockets.append(active_socket)
            self.logger.debug("Accepted logger from " + str(address))
            command_thread = Thread(target=self.__command_interpreter, args=(active_socket,))
            command_thread.daemon = True
            command_thread.start()
            self.active_threads.append(command_thread)

        for thr in self.active_threads:
            thr.join()
        log_thread.join()
        for sock in self.active_sockets:
            sock.close()
        log_socket.close()
        command_socket.close()

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
        while not self.shutdown:
            self.__engine_socket.send_string("Hello")
            ack = self.__engine_socket.recv_string()
            if ack != "OK":
                print("[D] ACK error")
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
