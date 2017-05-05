#!/usr/bin/python3
""" Manager

Component responsible for organizing the DB, test file operations
test plans generation.
"""

from __future__ import print_function

class EllidaManager(object):
    """ Test management component.
    Add, remove, change tests; generate test plans based on availbale metadata.
    """
    def __init__(self):
        print("Ellida manager initializing")

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

def main():
    """ Main """
    mgr = EllidaManager()
    mgr.add_test()
    mgr.rm_test()

if __name__ == '__init__':
    main()
