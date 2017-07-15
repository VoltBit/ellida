
from abc import ABCMeta, abstractmethod

import sys
sys.path.append('/usr/bin/python3.5/site-packages/')
sys.path.append('/usr/bin/python2.7/site-packages/')

class Provider(object):
    __metaclass__ = ABCMeta
    DEFAULT_LOG_NAMEFILE = "/tmp/ellida.log"

    def __init__(self):
        pass

    @abstractmethod
    def send_command(self, command):
        raise NotImplementedError()

    @abstractmethod
    def get_result_log(self):
        raise NotImplementedError()

    @abstractmethod
    def _start_test(self):
        raise NotImplementedError()

    @abstractmethod
    def cleanup(self):
        raise NotImplementedError()
