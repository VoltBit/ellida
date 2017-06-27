
from __future__ import print_function
import subprocess
from provider import Provider

class LtpProvider(Provider):
    ''' Provider class for the LTP package '''
def __init__(self, log_filename=Provider.DEFAULT_LOG_NAMEFILE): super(LtpProvider, self).__init__() self.log_filename = log_filename
        self.log_handle = open(log_filename, 'r+')
        self.command = 'echo "LTP test debug message"'

    def send_command(self, command):
        # self.command = command
        self._start_test(command)

    def get_result_log(self):
        result = self.log_handle.read()
        return result

    def _start_test(self, command):
        ltp_proc = subprocess.Popen(command, stdout=self.log_handle,
                                    stderr=self.log_handle)
        print("LTP proc returned: [", str(ltp_proc), "]")

    def cleanup(self):
        self.log_handle.close()

def main():
    print("Running LTP")
    provider = LtpProvider()
    provider.send_command(['echo', 'test'])
    print("Log contents: ", provider.get_result_log())

if __name__ == "__main__":
    main()
