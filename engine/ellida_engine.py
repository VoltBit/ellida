"""
Engine used for processing test plans.
"""
class EllidaEngine(object):
    """ Main class.
    """
    def start(self):
        """
        Initialization
        """
        print("Ellida engine started")

        print("Ellida engine stopped")


def main():
    en = EllidaEngine()
    en.start()

if __name__ == '__main__':
    main()
