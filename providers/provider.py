
from abc import ABCMeta, abstractmethod

import sys
sys.path.append('/usr/bin/python3.5/site-packages/')
sys.path.append('/usr/bin/python2.7/site-packages/')

class Provider(object):
    """ TODO """
    __metaclass__ = ABCMeta
    GLOBAL_LOG_NAMEFILE = "/opt/logs/ellida.log"

    def __init__(self):
        pass

    @abstractmethod
    def execute(self, targets):
        """ TODO """
        raise NotImplementedError()

    @abstractmethod
    def _start_test(self, command=None):
        """ TODO """
        raise NotImplementedError()

    @abstractmethod
    def cleanup(self):
        """ TODO """
        raise NotImplementedError()
