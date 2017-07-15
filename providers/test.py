from __future__ import print_function

from ltp_provider import LtpProvider
from ellida.engine.ellida_engine import EllidaEngine

class ProviderTest(object):

	def ltp_test(self):
		control = LtpProvider()
		control.execute(command)

def main():
	tester = ProviderTest()
	tester.ltp_test()

if __name__ == "__main__":
	main()
