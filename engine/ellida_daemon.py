#!/usr/bin/python3

import socket
import logging
import signal
import sys
from time import sleep
from daemonize import Daemonize
from threading import Thread

class EllidaDaemon(object):
    """ Daemon object that runs on target machine and manages communication between Ellida engine and the target
    [x] Main method that daemonizes and spawns two threads
    [x] Listening thread that waits for commands (to run tests)
    [x] Sender thread to send the logs back to the engine
    """
    proc_pid = "../res/ellida.pid"
    engine_addr = "192.168.7.1"
    local_addr = "192.168.7.2"
    # engine_addr = "192.168.10.7"
    # local_addr = "192.168.10.4"
    log_port = 9779
    comm_port = 9778
    log_results = ["log_test1", "log_test2"]
    shutdown = False

    def __init__(self):
        self.__log_setup()
        self.active_threads = []
        self.active_sockets = []

    def signal_handler(self, signal, frame):
        self.logger.debug("Ellida daemon shuting down")
        self.shutdown = True
        sys.exit(0)

    def __log_setup(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        fh = logging.FileHandler("/tmp/test.log", "w")
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

    def __daemon_thread(self):
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
        command_socket.listen()
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

    def daemon_start(self):
        self.logger.debug("Starting the daemon")
        signal.signal(signal.SIGINT, self.signal_handler)
        self.__daemon_thread()
        # try:
        #   print(self.log_fds)
        #   self.daemon = Daemonize(app="ellida_daemon", pid=self.proc_pid, action=self.__daemon_thread, keep_fds=self.log_fds)
        #   self.daemon.start()
        # except Exception as e:
        #   self.logger.debug(e)

def main():
    ellida_daemon = EllidaDaemon()
    ellida_daemon.daemon_start()

if __name__ == '__main__':
    main()