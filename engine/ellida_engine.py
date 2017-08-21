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
sys.path.append('../../')

from ellida.manager.ellida_manager import EllidaManager
from ellida.settings import EllidaSettings

print_lock = Lock()

class EllidaEngine(Process):
    """
    Ellida engine. Builds scripts that run the tests.
    """
    shutdown = False

    _EXEC = "req_exe"

    def __init__(self):
        self.colour = Fore.BLUE
        self.__opened_threads = []
        self.__sockets = []
        self.__clients = []
        # self.__network_setup()
        EllidaEngine.shutdown = False
        print("Ellida engine initialized.")

    def tprint(self, out_str, colour=""):
        print_lock.acquire()
        sys.stdout.write(colour + out_str)
        sys.stdout.flush()
        print_lock.release()

    def kill_handler(self, signal, frame):
        print("Engine shuting down")
        self.shutdown = True
        print("Engine shuting down...")
        for sock in self.__sockets:
            sock.close()
        for thr in self.__opened_threads:
            print("*")
            thr.join(1000)
            if thr.is_alive():
                print(Fore.RED + "could not join", thr)
            else:
                print("joined", thr)
        print("exiting")
        sys.exit(0)

    def __manager_comm(self):
        msg = self.__manager_socket.recv_string()
        self.tprint("[M]: ", Fore.YELLOW)
        self.tprint(msg + '\n')

    def __daemon_comm(self):
        msg = self.__daemon_socket.recv_string()
        if "init" in msg:
            client_id = msg.split('_')[1]
            if client_id not in self.__clients:
                self.__clients.append(client_id)
                self.tprint("[D]: " + str(client_id) + " joined\n", Fore.RED)
        elif "exit" in msg:
            client_id = msg.split('_')[1]
            self.__clients.remove(client_id)
            self.tprint("[D]: " + str(client_id) + " left\n", Fore.RED)
        else:
            self.tprint("[D]: ", Fore.RED)
            self.tprint(msg + '\n')

    def __drop_test(self, packet):
        if 'addr' not in packet or 'port' not in packet:
            # TODO
            print(Fore.RED + "No information about the connection for request:", packet)
            sys.exit(1)
        fsock = self.__context.socket(zmq.PAIR)
        self.__sockets.append(fsock)
        fsock.connect("tcp://" + packet['addr'] + ':' + packet['port'])
        fsock.send(bytes("No client connected (no daemon running)", 'utf-8'))
        fsock.send(bytes("ELLIDA_EXIT", 'utf-8'))
        fsock.close()

    def __ui_comm(self):
        packet = json.dumps({})
        packet = self.__ui_socket.recv_json()
        packet = json.loads(packet)
        self.tprint("[U]: ", Fore.BLUE)
        self.tprint(packet['event'] + ": " + str(packet['value']) + '\n')
        if packet['event'] == self._EXEC:
            if not self.__clients:
                self.__drop_test(packet)
            try:
                self.__daemon_socket.send_json(packet, zmq.NOBLOCK)
                print("Sending ", packet, " to daemon")
            except:
                pass

    def __run_set(self, test_set):
        """ TODO """
        test_set = {
            'spec': "agl",
            'layer': "services",
            'provider': "ltp",
            'req': "",
        }

    def __network_setup(self):
        self.__context = zmq.Context()
        self.__ui_socket = self.__context.socket(zmq.PAIR)
        self.__ui_socket.bind("tcp://*:%s" % EllidaSettings.UI_SOCKET)
        self.__daemon_socket = self.__context.socket(zmq.PAIR)
        self.__daemon_socket.bind("tcp://" + EllidaSettings.DAEMON_ADDR + ":" +
                                  str(EllidaSettings.DAEMON_SOCKET))
        self.__manager_socket = self.__context.socket(zmq.PAIR)
        self.__manager_socket.bind("tcp://*:%s" % EllidaSettings.MANAGER_SOCKET)
        self.__poller = zmq.Poller()
        self.__poller.register(self.__ui_socket, zmq.POLLIN)
        self.__poller.register(self.__daemon_socket, zmq.POLLIN)
        self.__poller.register(self.__manager_socket, zmq.POLLIN)

    def start_engine(self):
        # signal.signal(signal.SIGINT, self.kill_handler)
        self.__network_setup()
        while not EllidaEngine.shutdown:
            sockets = dict(self.__poller.poll())
            if sockets.get(self.__ui_socket) == zmq.POLLIN:
                self.__ui_comm()
                # ui_thr = Thread(target=self.__ui_comm, daemon=True)
                # ui_thr.start()
                # self.__opened_threads.append(ui_thr)
            if sockets.get(self.__daemon_socket) == zmq.POLLIN:
                self.__daemon_comm()
                # d_thr = Thread(target=self.__daemon_comm)
                # d_thr.start()
                # self.__opened_threads.append(d_thr)
            if sockets.get(self.__manager_socket) == zmq.POLLIN:
                self.__manager_comm()
                # man_thr = Thread(target=self.__manager_comm)
                # man_thr.start()
                # self.__opened_threads.append(man_thr)

def main():
    engine = EllidaEngine()
    engine.start_engine()

if __name__ == "__main__":
    main()
