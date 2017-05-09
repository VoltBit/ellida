"""
Engine used for processing test plans.
"""
class EllidaEngine(object):
	""" Main class.
	"""
	def start_engine(self):
		"""
		Initialization
		"""
		print("Ellida engine started")

		print("Ellida engine stopped")

	@classmethod
	def build_ltp(cls):
		pass

	@classmethod
	def build_imagetest(cls):
		pass

	@classmethod
	def start_engine(cls):
		print("Ellida engien started")

def main():
	en = EllidaEngine()
	en.start()

if __name__ == '__main__':
	main()
