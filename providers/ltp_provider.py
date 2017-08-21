""" LTP provider module """

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

class LtpProvider(Provider):
    """ Provider class for the LTP package """

    __BASE_CMD = "/opt/ltp/runltp -pq -l "
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
            command = self.__BASE_CMD + self.__gen_logfile() + " -f " + target
            print("LTPProvider executing command:", command)
            result = self._start_test(command)
            results.append(result)
        return results

    def get_raw_result(self):
        result = self.log_handle.read()
        return result

    def get_ellida_result(self):
        pass

    def get_result(self, type=None):
        pass

    def _start_test(self, command=None):
        ltp_proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res, err = ltp_proc.communicate()
        # res = res.decode('utf-8')
        # print(res)
        print("code:", ltp_proc.returncode)
        return res
        # ltp_proc_ret_code = subprocess.check_call(command.split())
        # res = subprocess.call(command.split())
        # print("res:", res)
        # test_result = subprocess.check_output(command.split())
        # print(test_result.data)
        # test_result = None
        # try:
        #     test_result = subprocess.check_output(command.split())
        #     print(test_result.data)
        # except Exception as e:
        #     pass
            # test_result = e
            # print("Result type: ", type(test_result.data))
            # print("Process return code:", test_result.returncode)

    def cleanup(self):
        self.log_handle.close()

def main():
    provider = LtpProvider()
    provider.send_command(['echo', 'test'])

if __name__ == "__main__":
    main()
