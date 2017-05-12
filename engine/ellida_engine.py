"""
Engine used for processing test plans.
Next todo:

[] Generate dummy running scripts for LTP and image tests.
    [] Setup Image Tests: copy tests in the right directory, config file with
    the list of tests
    [] 
[] Should support:
    [] Selenium
    [] LTTng
    [] perf
    [] systemtap -> cum controlez sau inserez module de kernel?
"""
import sys
sys.path.append('/home/smith/Dropbox/')
import os
import shutil
from ellida.manager.ellida_manager import EllidaManager

class EllidaEngine(object):
    """ Ellida engine. Builds scripts that run the tests.
    """
    build_path = "build/"
    build_handlers = []
    poky_build = "/home/smith/projects/poky/build/"

    def __init__(self):
        self.manager = EllidaManager()
        self.supported_specs = self.manager.get_specs()
        self.__setup()
        print("Ellida engine initialized.")

    def __setup(self):
        os.makedirs(self.build_path, exist_ok=True)
        # os.makedirs(self.build_path)
        for spec in self.supported_specs:
            self.build_handlers.append(open(self.build_path + str(spec) +
                                            ".sh", "w+"))

    @classmethod
    def build_ltp(cls):
        pass

    @classmethod
    def build_imagetest(cls):
        pass

    def start_engine(self):
        """
        1. Folosesc managerul ca sa parsez specificatia
        2. Iau arborele de dependinte si il parcurg
        3. Generez scripturi de configurare si rulare pentru Image Tests.
        """
        spec_graphs = self.manager.parse_specifications()
        for spec, graph in spec_graphs.items():
            print("Spec: ", spec, "\n", graph)

    def close_engine(self):
        """ Do cleanup.
        """
        for handle in self.build_handlers:
            handle.close()
        shutil.rmtree(self.build_path)

    def __setup_image_tests(self):
        """
        1. copy scripts
        2. add list of scripts to file
        """
        pass


def main():
    """ Main function.
    """
    engine = EllidaEngine()
    engine.start_engine()

if __name__ == '__main__':
    main()
