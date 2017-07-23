""" TODO """

from __future__ import print_function

import subprocess
import sys
import json
from datetime import datetime

sys.path.append('/usr/bin/python3.5/site-packages/')
sys.path.append('/usr/bin/python2.7/site-packages/')

# from ellidadaemon.providers.provider import Provider
from ellida.providers.provider import Provider

class LtpProvider(Provider):
    ''' Provider class for the LTP package '''

    __BASE_CMD = "/opt/ltp/runltp -p -l "
    __TARGET_ROOT = "/opt/ellida_tests/"
    __LOG_ROOT = "/opt/logs/"

    def __init__(self, log_filename=Provider.GLOBAL_LOG_NAMEFILE):
        super(LtpProvider, self).__init__()
        self.log_filename = log_filename
        self.log_handle = open(log_filename, 'a+')
        self.spec = None

    def configure(self, config):
        self.spec = config['spec']
        self.req = config['req']
        self.set_no = config['set']

    def __gen_logfile(self):
        timest = datetime.now().strftime('%H:%M_%d.%m.%Y.log')
        self.log_filename = self.__LOG_ROOT + self.spec +\
            "_" + self.req + "_" + str(self.set_no) + "_" + str(timest)
        self.log_handle = open(self.log_filename, 'a+')
        return self.log_filename

    def execute(self, targets):
        for target in targets:
            command = self.__BASE_CMD + self.__gen_logfile() + " -f " + self.__TARGET_ROOT + target
            # command = self.__BASE_CMD + self.log_filename + " -f " + self.__TARGET_ROOT + target
            print("executing command:", command)
            self._start_test(command)

    def get_raw_result(self):
        result = self.log_handle.read()
        return result

    def get_ellida_result(self):
        pass

    def get_result(self, type=None):
        pass

    def _start_test(self, command=None):
        ltp_proc = subprocess.Popen(command.split(), stdout=self.log_handle,
                                    stderr=self.log_handle)
        ltp_proc.communicate()
        print("LTP proc returned: [", str(ltp_proc.returncode), "]")

    def cleanup(self):
        self.log_handle.close()

def main():
    print("Running LTP")
    provider = LtpProvider()
    provider.send_command(['echo', 'test'])
    print("Log contents: ", provider.get_result_log())

if __name__ == "__main__":
    main()
