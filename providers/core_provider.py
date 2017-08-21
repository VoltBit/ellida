""" Core provider module """

from __future__ import print_function

import subprocess
import sys
import json
import os
from datetime import datetime

sys.path.append('/usr/bin/python3.5/site-packages/')
sys.path.append('/usr/bin/python2.7/site-packages/')
sys.path.append('../../')

# from ellidadaemon.providers.provider import Provider
from ellida.providers.provider import Provider

class CoreProvider(Provider):
    """ Provider class for running Python scripts """
    __BASE_CMD = "python -B "
    __TARGET_ROOT = "/opt/ellida_tests/"
    __LOG_ROOT = "/opt/logs/"

    def __init__(self, log_filename=Provider.GLOBAL_LOG_NAMEFILE):
        super(CoreProvider, self).__init__()
        self.log_filename = log_filename
        self.log_handle = open(log_filename, 'a+')
        self.spec = None

    def configure(self, config):
        self.spec = config['spec']
        self.req = config['req']
        self.set_id = config['set']

    def __gen_logfile(self):
        timest = datetime.now().strftime('%H:%M_%d.%m.%Y.log')
        self.log_filename = self.__LOG_ROOT + self.spec +\
            "_" + self.req + "_" + self.set_id + "_" + str(timest)
        print("using logfile: ", self.log_filename)
        self.log_handle = open(self.log_filename, 'a+')
        return self.log_filename

    def execute(self, targets):
    	results = []
        for target in targets:
            command = self.__BASE_CMD + target
            # command = self.__BASE_CMD + target + ' 2>&1 ' + self.__gen_logfile()
            print("CoreProvider executing command:", command)
            result = self._start_test(command)
            results.append(result)
        return results

	def _start_test(self, command=None):
		pass

	def cleanup(self):
        self.log_handle.close()