#!/usr/bin/python3
"""
Full system initializer.

Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
"""

from __future__ import print_function
import sys
import multiprocessing
import logging
import signal


sys.path.append('/home/smith/Dropbox/')
from ellida.engine.ellida_engine import EllidaEngine
from ellida.engine.ellida_daemon import EllidaDaemon
from ellida.manager.ellida_manager import EllidaManager
from ellida.settings import EllidaSettings
from ellida.frontend.ellida_ui import EllidaUi


class EllidaInit(object):
    """
    Initializer object base on the multiprocessing module. Spawn processes for
    all the major components of the system.
    """

    def __init__(self):
        multiprocessing.log_to_stderr()
        self.logger = multiprocessing.get_logger()
        self.logger.setLevel(logging.INFO)

    def kill_handler(self, signal, frame):
        """
        Handle the sigint signal.
        """
        self.shutdown()
        sys.exit(0)

    def start(self):
        """
        Start the whole system with its main components - manager, engine
        and UI as separate processes.
        """
        signal.signal(signal.SIGINT, self.kill_handler)
        engine = EllidaEngine()
        daemon = EllidaDaemon()
        manager = EllidaManager()
        gui = EllidaUi()

        self.engine_process = multiprocessing.Process(target=engine.start_engine)
        self.manager_process = multiprocessing.Process(target=manager.start_manager)
        self.daemon_process = multiprocessing.Process(target=daemon.start_daemon)
        self.gui_process = multiprocessing.Process(target=gui.ui_init)
        self.engine_process.start()
        self.daemon_process.start()
        self.manager_process.start()
        self.gui_process.start()

        self.gui_process.join()
        self.daemon_process.join()
        self.manager_process.join()
        self.engine_process.join()

    def shutdown(self):
        """
        Shutdown all processes and exit.
        """
        # self.gui_process.join(5)

        if self.engine_process.is_alive():
            self.engine_process.terminate()
        if self.manager_process.is_alive():
            self.manager_process.terminate()
        if self.daemon_process.is_alive():
            self.daemon_process.terminate()
        if self.gui_process.is_alive():
            self.gui_process.terminate()

def main():
    initializer = EllidaInit()
    initializer.start()

if __name__ == '__main__':
    main()
