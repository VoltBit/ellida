#!/usr/bin/python3
""" Manager

Component responsible for organizing the DB, test file operations
test plans generation.
"""

from __future__ import print_function
import json
import os

class EllidaManager(object):
	""" Test management component.
	Add, remove, change tests; generate test plans based on availbale metadata.
	"""

	database_path = "../database/"
	meta_database_file = "database.json"
	build_path = "build/"
	supported_specs = []
	spec_hadlers = []
	build_handlers = []

	def __init__(self):
		self.__get_supported_specifications()
		self.__setup()

	@classmethod # <<<< what happens if somone useses more than one manager in a single application?
	def __setup(cls):
		os.makedirs(build_path, exists_ok=True)
		build_handlers.append(open(build_path + "agl.sh")) # <<<<<<<<<< change this to something more generic

	@classmethod
	def __cleanup(cls):
		for handler in build_handlers:
			close(handler)

	@classmethod
	def __get_supported_specifications(cls):
		with open(cls.database_path + cls.meta_database_file) as meta_database:
			data = json.load(meta_database)
		cls.supported_specs = data['specs']

	@classmethod
	def add_test(cls):
		""" Add a test.
		Input: """
		print("test adding")

	@classmethod
	def rm_test(cls):
		""" Remove a test.
		Input: """
		print("test removal")

	@classmethod
	def ch_test(cls):
		""" Change a test.
		Input: """
		print("test change")

	@classmethod
	def parse_specification(cls):
		file_list = []
		spec_data = []
		""" Parse database directory tree. """
		for spec in cls.supported_specs:
			for root, dirs, files in os.walk(cls.database_path + spec):
				# print("root: ", root)
				# print("dirs: ", dirs)
				# print("files: ", files)
				file_list += files
		print("Files: ", file_list)
		for file in file_list:
			with open(file) as json_file:
				json.load(json_file)
				
	def start_manager(self):
		print("Ellida manager started")

def main():
	""" Main """
	mgr = EllidaManager()
	# mgr.add_test()
	# mgr.rm_test()
	mgr.parse_specification()

if __name__ == '__main__':
	main()
