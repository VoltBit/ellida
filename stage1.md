# Architecture

## Framework description

The framework provides a very specific functionality within Yocto environment - how well does a generated image meet the requirements of a given specification.

**Features**

 - Encapsulates two powerful testing facilities already present in Yocto - LTP and Image Tests
 - Abstracts the details of communication between the image and various tests, no matter what part of the framework provides the test
 - Can be controlled by Yocto via meta-ellida layer - specification type, custom specification
 - Ensures configuration of components via classes and recipes

<img src="res/arch.png" width=900>

### Legend

 - Green: to be implemented
 - Red: auto-generated
 - Blue: part of Yocto/OpenEmbedded ecosystem
 - Dashed: optional, nice to have

### Main components

**Test manager**

Component used to add or remove tests, change test details. The test manager contains meta-specification files which are test plans based on a specification and can also be configured.
Funcions:

 - Manage the test set
 - Provide test plans for the engine

A test plan consists simply of a plan ID, specification tag and list of tests (by test ID)

**Test set**

Information about the test is kept in some form of database. The set should be kept as JSON files as a full database system seems too much for the given task. The characteristics of a test should include:

 - Type (ex: unit, functional, benchmark)
 - Tag (AGL, CGL, custom)
 - ID
 - Source (LTP, IT)
 - Alias (optional, for ease of use inside a software framework TODO)
 - Arguments

Since LTP is a huge collection of tests it should be used as much as possible, for all tests not included in LTP or are not a perfect fit for some requirement, Image Tests should be used. The system is powerful enough to test just about anything, be it unit, functional or benchmarking. Any other system such as ptest can be integrated in the future.

**Test engine**

Made of:

1. JSON interpreter or database communication system for test fetching
2. Test filter based on test plans
3. Control script generator based on meta-specification files (test plans) - generates scripts based on current specification and available tests from the database and runs them

**Log interpreter**

Anything that is readable. Should not be dependent of log file paths or the tests should have a common log location and if possible a common format.

---

### Software components and existing solutions

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

- deeply integrated with Yocto, every recipe can provide a ptest in the form of a test script and a small addition to the recipe code
- ptests are run using the ptest-runner utility that should run inside a running image or device
```
ptest-runner [-d directory] [-l list] [-t timeout] [-h] [ptest1 ptest2 ...]
```

1.3. **LTP**

- very comprehensive suite of tests with more than 4000 tests
- the LTP suite comes in the form of C, C++ programs and shell scripts
- they are compiled and copied in /opt/ltp along with some scripts used for running the whole suite
- to make use of LTP the framework will create a command file such as:

```
#Tag       Test case
#---------------------------------------
mtest01     mtest01 -p 10
mmstress    mmstress -x 100
fork01      fork01
chdir01     symlink01 -T chdir01
#----------------------------------------
```

then the scripts inside are run from /opt/ltp with:

    ```
    ./runltp -p -l result.log -f my_command_file
    ```
- [Docs](http://ltp.sourceforge.net/documentation/how-to/ltp.php)

---

2. Platforms not integrated with Yocto

2.1. **Fuego** - solution based on Jenkins automation server

**Fuego test phases:**

        - pre_test
        - build
        - deploy
        - run
        - get_testlog
        - processing
        - post_test

<img src="http://bird.org/ffiles/fuego-test-phases.png" width=500>

- The tests are compiled, deployed and ran on the image via ssh or other channel of communication that was configured beforehand
- Adding a new target - physical or virtual device - is done through configuration files and a minimal setup on the device (create test directory)

- [Docs](http://bird.org/ffiles/fuego-docs.pdf)


---

### Implementation specific notes

ROOTFS_POSTPROCESS_COMMAND += "function1;...;functionN" - run shell functions as soon as the image build is done (for conf/local)
IMAGE_POSTPROCESS_COMMAND += "func" for classes
