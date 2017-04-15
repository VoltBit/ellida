# Architecture

## Software components and existing solutions

1. Testing layers, classes and recipes already integrated in Yocto

1.1. **Image tests**
    - Suite of Python tests that connect to target image via ssh and runs scripts based on the Python unittest module.
    - The build system has the ability to run a series of automated tests for qemu images.
    - All the tests are actually commands run on the target system over ssh.
    - The tests themselves are written in Python, making use of the unittest module.
    - The class that enables this is testimage.bbclass (which handles loading the tests and starting the qemu image)
    - Location of tests: meta/lib/oeqa/runtime

Best suited for the unit tests, most if not all of the unit tests can be completed through imagetests.bbclass. The framework should be able to:

    - Configure the system to be able to use image tests:
        - Add a set of tests that imagetests can use, the set should be added through a layer
        - runqemu script needs sudo access for setting up the tap interface, so you need to make sure it can do that non-interactively
            - manually configure a tap interface for your system
            - run as root the script in scripts/runqemu-gen-tapdev which should generate a list of tap devices (that's usually done in AutoBuilder-like setups)
        - the DISPLAY variable needs to be set so that means you need to have an X server available (e.g start vncserver for a headless machine)
        - some of the tests (in particular smart tests) start a http server on a random high number port, used to serve files to the target. The smart module serves ${DEPLOY_DIR}/rpm so it can run smart channel commands. That means your host's firewall must accept incoming connections from 192.168.7.0/24 (the default class used for tap0 devices by runqemu)

1.2. **Ptests**
    - deeply integrated with Yocto, every recepe can provide a ptest in the form of
1.3. **LTP**
    - very comprehensive suite of tests with more than 4000 tests
    - the LTP suite comes in the form of C, C++ programs and shell scripts
    - they are compiled and copied in /opt/ltp along with some scripts used for
    running the whole suite
    - [Docs](http://ltp.sourceforge.net/documentation/how-to/ltp.php)

2. Fuego - solution based on Jenkins automation server
    - Fuego test phases
        - pre_test
        - build
        - deploy
        - run
        - get_testlog
        - processing
        - post_test
    <img src="http://bird.org/ffiles/fuego-test-phases.png" width=500>

    - The tests are compiled, deployed and ran on the image via ssh or other
    channel of communicaton that was configured beforehand
    - Adding a new target - physical or virtual device - is done through
    configuration files and a minimal setup on the device (create test
    directory)

### Framework setup

1. Configure the desired specification - [ ] AGL | [ ] CGL
2. Install the parts needed to integrate with Yocto:
    - Create new layer if it does not exist
    - Add recipes for all needed software

3. After Yocto processes generate the target image, configure the communication medium
    - initially communicate via ssh - image tests already do so

### Features

The framework abstracts away a specification through a set of tests that try to emulate as closely as possible the requirements.
*** How should the framework integrate with Yocto? ***

Extensibility is vital, tests must be easy to add and remove, they should be easily accessible, easy to view and understand.



*** Building blocks ***
1. **Yocto** - Linux image generation based on configuration files called layers and recipies
2. **Tests** - Set of scripts and programs based on the AGL specification.

The framework will glue together all utilities necessary for a complete evaluation of a given specification. For each test there is a piece of software needed, ether already implemented in Yocto or that need to be written.

First, each test should be assigned to a testing method. To do this I need to understand how the software works. Mainly, I need to understand Image Tests (which I think I do), ptest, LTP, AutoBuild.

### Implementation specific notes

ROOTFS_POSTPROCESS_COMMAND += "function1;...;functionN" - run shell functions as soon as the image build is done (for conf/local)
IMAGE_POSTPROCESS_COMMAND += "func" for classes
