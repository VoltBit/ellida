"""
Engine used for processing test plans.
"""

"""
Next todo:

[] Generate dummy running scripts for LTP and image tests.
[] Should support:
	[] Selenium
	[] LTTng
	[] perf
	[] systemtap -> cum controlez sau inserez module de kernel? (nu se poate
	face din engine, doar conectaarea la module și verificare output-ulu)
"""

import ellida.manager.ellida_manager

class EllidaEngine(object):

	def __init__(self):
		self.__setup()

	""" Main class.
	"""
	def start_engine(self):
		"""
		Initialization
		"""
		print("Ellida engine started")

		print("Ellida engine stopped")

	@classmethod # <<<< what happens if somone useses more than one manager in a single application?
	def __setup(cls):
		os.makedirs(cls.build_path, exists_ok=True)
		build_handlers.append(open(build_path + "agl.sh")) # <<<<<<<<<< change this to something more generic

	@classmethod
	def build_ltp(cls):
		pass

	@classmethod
	def build_imagetest(cls):
		pass

	@classmethod
	def start_engine(cls):
		print("Ellida engine started")

def main():
	en = EllidaEngine()
	en.start()

if __name__ == '__main__':
	main()
