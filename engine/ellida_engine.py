#!/usr/bin/python3

"""
Engine used for processing test plans.
"""

from __future__ import print_function
import os
import sys
import json
import shutil
import subprocess
import socket
import signal
from time import sleep
from threading import Thread, Lock
from multiprocessing import Process
import zmq

from colorama import init, Fore
init(autoreset=True)

sys.path.append('/home/smith/Dropbox/')
sys.path.append('/home/adobre/Dropbox/')
from ellida.manager.ellida_manager import EllidaManager
from ellida.settings import EllidaSettings

print_lock = Lock()

class EllidaEngine(Process):
    """
    Ellida engine. Builds scripts that run the tests.
    """
    shutdown = False

    def __init__(self):
        self.colour = Fore.BLUE
        # self.__network_setup()
        EllidaEngine.shutdown = False
        print("Ellida engine initialized.")

    def kill_handler(self, signal, frame):
        print("Engine shuting down")
        self.shutdown = True
        self.close_engine()
        sys.exit(0)

    def __manager_comm(self):
        msg = self.__manager_socket.recv()
        if msg:
            self.__manager_socket.send_string("OK")
        print_lock.acquire()
        print(Fore.YELLOW + "[M]")
        print(msg)
        print_lock.release()

    def __daemon_comm(self):
        msg = self.__daemon_socket.recv()
        if msg:
            self.__daemon_socket.send_string("OK")
        print_lock.acquire()
        print(Fore.RED + "[D]")
        print(msg)
        print_lock.release()

    def __ui_comm(self):
        print_lock.acquire()
        msg = self.__ui_socket.recv()
        if msg:
            self.__ui_socket.send_string("OK")
        print(Fore.BLUE + "[U]")
        print(msg)
        print_lock.release()

    def __run_set(self, test_set):
        test_set = {
            'spec': "agl",
            'layer': "services",
            'provider': "ltp",
            'req': "",
        }

    def __network_setup(self):
        context = zmq.Context()
        self.__ui_socket = context.socket(zmq.PAIR)
        self.__ui_socket.bind("tcp://*:%s" % EllidaSettings.UI_SCOKET)
        self.__daemon_socket = context.socket(zmq.PAIR)
        self.__daemon_socket.bind("tcp://" + EllidaSettings.DAEMON_ADDR + ":" +
                                  str(EllidaSettings.DAEMON_SOCKET))
        self.__manager_socket = context.socket(zmq.PAIR)
        self.__manager_socket.bind("tcp://*:%s" % EllidaSettings.MANAGER_SOCKET)
        self.__poller = zmq.Poller()
        self.__poller.register(self.__ui_socket, zmq.POLLIN)
        self.__poller.register(self.__daemon_socket, zmq.POLLIN)
        self.__poller.register(self.__manager_socket, zmq.POLLIN)

    def start_engine(self):
        signal.signal(signal.SIGINT, self.kill_handler)
        self.__network_setup()
        while not EllidaEngine.shutdown:
            sockets = dict(self.__poller.poll())
            if sockets.get(self.__ui_socket) == zmq.POLLIN:
                self.__ui_comm()
            if sockets.get(self.__daemon_socket) == zmq.POLLIN:
                self.__daemon_comm()
            if sockets.get(self.__manager_socket) == zmq.POLLIN:
                self.__manager_comm()

    def close_engine(self):
        pass

def main():
    engine = EllidaEngine()
    engine.start_engine()

if __name__ == "__main__":
    main()


    # def __network_setup(self):
    #     context = zmq.Context()

    #     manager_thread = Thread(target=self.__manager_comm, args=(context,))
    #     manager_thread.daemon = True
    #     manager_thread.start()
    #     daemon_thread = Thread(target=self.__daemon_comm, args=(context,))
    #     daemon_thread.daemon = True
    #     daemon_thread.start()
    #     ui_thread = Thread(target=self.__ui_comm, args=(context,))
    #     ui_thread.daemon = True
    #     ui_thread.start()

    #     ui_thread.join()
    #     daemon_thread.join()
    #     manager_thread.join()
    #     print(Fore.GREEN + "All threads are down")
