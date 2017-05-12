#!/usr/bin/python3
""" Manager

Component responsible for organizing the DB, test file operations
test plans generation.

The meta land.

meta-specification (abstractization) -> folder tree
meta-mapping (the spec "superblock") ->
"""

import json
import os
import sys
sys.path.append('/home/smith/Dropbox/')
from ellida.manager.depg import DepGraph
from ellida.spec_parser import SpecParser

"""
[x] Complete spec parse from database => list
[] Map tests to parsed database (append characteristics to the list) ->
how?
[] See if file read and writes can be diminished
[] Try to only open files once at the initialization of the object and close on exit
the path to the tests should be set inside the JSON
-> the manager should generate a database based on physical locations
-> ideally: both the set of tests and the LTP tests would contain a label and
the JSON will only provide a label
-> labels could be just the name of the requirement
-> the manager has to have an internal mapping between tests and specification
directory tree

exceptions:
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
    spec_database = {} # list of specs, each spec is a list of JSON objects
    spec_graphs = {}

    def __init__(self):
        self.__get_supported_specifications()

    @classmethod
    def __cleanup(cls):
        # for handler in cls.build_handlers:
        #   handler.close()
        pass

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

    """
    {
      "id": "AVL.2.0",
      "name": "Single-bit ECC handling",
      "spec": "CGL",
      "priority": "P2",
      "category": "availability",
      "type": "unit",
      "dependencies": [],
      "description": ""
    }

    {
        "specs": ["agl", "cgl"],
        "mapping": {
            "AVL.2.0": [{
                "path": "cgl_avl_example.py",
                "source": "it"
            }],
            "SMM.3.1": [{
                "path": "cgl_smm_example.py",
                "source": "it"
            }]
        }
    }
    """

    def get_specs(self):
        """ Return a list of the supported specifications.
        """
        return self.supported_specs

    @classmethod
    def __check_test_files(cls, files):
        for test_file in files:
            if not os.path.exists(test_file['path']):
                raise EllidaManagerError("No such file " + test_file['path'])

    def add_tests(self, requirement_id, test_list):
        """ Add a tests to a requirement.
        """
        if requirement_id not in self.mapping.keys():
            raise EllidaManagerError("Unknown requirement")
        self.__check_test_files(test_list)
        self.mapping[requirement_id] += test_list

    def add_tests_json(self, test_data):
        """ Adds information about test files to a requirement.
        Format:
        {
            id: "requirement_id"
            tests: [{path: "", source: ""}],
        }
        """
        if test_data['id'] not in self.mapping.keys():
            raise EllidaManagerError("Unknown requirement")
        self.__check_test_files(test_data['tests'])
        self.mapping[test_data['id']] += test_data['tests']

    def add_requirement(self, test_id, name, spec, priority, category, test_type,
                        dependencies, description):
        """ Add a requirement to database, changes the spec abstartization structure
        and the meta-mapping.
        """
        new_entry = {}
        new_entry['id'] = test_id
        new_entry['name'] = name
        new_entry['spec'] = spec
        new_entry['priority'] = priority
        new_entry['category'] = category
        new_entry['type'] = test_type
        new_entry['dependencies'] = dependencies
        if not description:
            description = ""
        new_entry['description'] = description
        self.spec_database[spec].append(new_entry)
        print("Added test with ID ", str(test_id))

    def add_requirement_json(self, json_data):
        """ Add a test received in the form of a JSON object.
        """
        fields = ['id', 'name', 'spec', 'priority', 'category', 'type',
                  'dependencies', 'description']
        if len(set(fields).intersection(set(json_data.keys()))) != len(fields):
            raise EllidaManagerError("New test format error, fields mismatch")
        for field in fields:
            if field != 'description' and not json_data[field]:
                raise EllidaManagerError("New test format error, empty fields")
        self.spec_database[json_data['spec']].append(json_data)
        print("Added test with ID ", str(json_data['id']))

    def rm_test(self, spec, test_id):
        """ Remove a test.
        """
        if not spec or not test_id:
            raise EllidaManagerError("Invalid operation: specificaion and id\
                    required for test remove")
        if spec not in self.supported_specs:
            raise EllidaManagerError("Test removal exception - specification does not exist.")
        print("database: ", self.database_path)
        print("test ", str(test_id), " removed")

    def ch_test(self, spec, test_id):
        """ Change a test.
        Input: """
        print("test change")

    @classmethod
    def __gen_dependency_graph(cls, spec_tests):
        graph = DepGraph()
        for req in spec_tests:
            graph.add_node(req['id'])
            if req['dependencies']:
                graph.add_dependency(req['id'], req['dependencies'], True)
        return graph

    def parse_specifications(self):
        """ Parse database directory tree.
        """
        file_list = []
        for spec in self.supported_specs:
            self.spec_database[spec] = []
            for root, _, files in os.walk(self.database_path + spec):
                for current_file in files:
                    file_list.append(os.path.join(root, current_file))
                    with open(os.path.join(root, current_file)) as json_file:
                        self.spec_database[spec].append(json.load(json_file))
            self.spec_graphs[spec] = self.__gen_dependency_graph(self.spec_database[spec])
        return self.spec_graphs

    def parse_specification(self, spec):
        """ Parse database directory tree and return dependecny tree for a
        give specification.
        """
        file_list = []
        self.spec_database[spec] = []
        for root, _, files in os.walk(self.database_path + spec):
            for current_file in files:
                file_list.append(os.path.join(root, current_file))
                with open(os.path.join(root, current_file)) as json_file:
                    self.spec_database[spec].append(json.load(json_file))
        self.spec_graphs[spec] = self.__gen_dependency_graph(self.spec_database[spec])
        return self.spec_graphs[spec]

    @classmethod
    def start_manager(cls):
        """ Handler to be used at framework startup.
        """
        print("Ellida manager started")

    @classmethod
    def close_manager(cls):
        """ Class handler for framework closing.
        """
        cls.__cleanup()
        print("Ellida manager closed")

def main():
    """ Main """
    SpecParser.parse_cgl()
    mgr = EllidaManager()
    mgr.parse_specifications()

if __name__ == '__main__':
    main()

class EllidaManagerError(Exception):
    def __init__(self, message = "Ellida manager error"):
        self.message = "[M] " + message
