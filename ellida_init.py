#!/usr/bin/python3.5
"""
Full system initializer.
"""

from __future__ import print_function
import sys
import multiprocessing
from ellida.engine.ellida_engine import EllidaEngine

from ellida.frontend.ellida_ui import EllidaUi
sys.path.append('/home/smith/Dropbox/')

import zmq

class EllidaInit(object):
    """
    Initializer object base on the multiprocessing module. Spawn processes for
    all the major components of the system.
    """

    @classmethod
    def start(cls):
        engine = EllidaEngine()
        gui = EllidaUi()
        gui_process = multiprocessing.Process(target=gui.ui_init)
        gui_process.start()
        engine_process = multiprocessing.Process(target=engine.start_engine)
        engine_process.start()

        engine_process.join()
        gui_process.join()

def main():
    EllidaInit.start()

if __name__ == '__main__':
    main()
