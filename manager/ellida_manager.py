#!/usr/bin/python3
""" Manager

Component responsible for organizing the DB, test file operations
test plans generation.
"""

from __future__ import print_function
import json
import os
# import igraph
import depg
# import ellida.manager.depg

"""
Next todo:

[x] Complete spec parse from database => list
[] Map tests to parsed database (append characteristics to the list) -> how? the path to the tests should be set inside the JSON
-> the manager should generate a database based on physical locations
-> ideally: both the set of tests and the LTP tests would contain a label and the JSON will only provide a label
-> labels could be just the name of the requirement
-> the manager has to have an internal mapping between tests and specification directory tree


[] Make a dependency tree with the (list)
[] Establish connection with engine

+ good to have: ecah JSON file should be usable on its own, however if information about
specification is missing the information could be deduced from the folder tree structure - parent folders and subfolders

how to write custom exceptions:
https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions

"""

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
	spec_database = {} # list of specs, each spec is a list of JSON objects (list of dict)
	spec_graphs = {}

	def __init__(self):
		self.__get_supported_specifications()

	@classmethod
	def __cleanup(cls):
		for handler in build_handlers:
			close(handler)

	@classmethod
	def __get_supported_specifications(cls):
		""" Parse the superfile and provide a list of supported specifications.
		"""
		with open(cls.database_path + cls.meta_database_file) as meta_database:
			data = json.load(meta_database)
		cls.supported_specs = data['specs']
		cls.mapping = data['mapping']
		print("Supported specs: ", cls.supported_specs)
		print("mapping: ", cls.mapping)

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

	def __gen_dependency_graph(self, spec_tests):
		G = depg.DepGraph()
		for req in spec_tests:
			G.add_node(req['id'])
			if req['dependencies']:
				G.add_dependency(req['id'], req['dependencies'], True)
		return G

	def parse_specification(self):
		""" Parse database directory tree.
		"""
		file_list = []
		spec_data = []
		for spec in self.supported_specs:
			self.spec_database[spec] = []
			for root, dirs, files in os.walk(self.database_path + spec):
				for file in files:
					file_list.append(os.path.join(root, file))
					with open(os.path.join(root, file)) as json_file:
						self.spec_database[spec].append(json.load(json_file))
			self.spec_graphs[spec] = self.__gen_dependency_graph(self.spec_database[spec])
			print(self.spec_graphs[spec])
		# print("Database: ", self.spec_database)

	def start_manager(self):
		print("Ellida manager started")

	def close_manager(slef):
		self.__cleanup()
		print("Ellida manager closed")

def main():
	""" Main """
	mgr = EllidaManager()
	# mgr.add_test()
	# mgr.rm_test()
	mgr.parse_specification()

if __name__ == '__main__':
	main()
