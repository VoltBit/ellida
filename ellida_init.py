#!/usr/bin/python3.5
"""
Full system initializer.
"""

from __future__ import print_function
import sys
import multiprocessing
import logging
import signal

sys.path.append('/home/smith/Dropbox/')
from ellida.engine.ellida_engine import EllidaEngine
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
        signal.signal(signal.SIGINT, signal_handler)

    def kill_handler(self):
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
        engine = EllidaEngine()
        gui = EllidaUi()
        self.gui_process = multiprocessing.Process(target=gui.ui_init)
        self.gui_process.start()
        self.engine_process = multiprocessing.Process(target=engine.start_engine)
        self.engine_process.start()
        self.manager_process = multiprocessing.process(target=manager.start_manager)
        self.manager_process.start()

        self.manager_process.join()
        self.engine_process.join()
        self.gui_process.join()

    def shutdown(self):
        """
        Shutdown all processes and exit.
        """
        self.gui_process.shutdown()
        self.manager_process.shutdown()
        self.engine_process.shutdown()

def main():
    EllidaInit.start()

if __name__ == '__main__':
    main()
