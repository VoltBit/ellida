import unittest
import os
from oeqa.oetest import oeRuntimeTest, skipModule
from oeqa.utils.decorators import *

def setUpModule():
    if not oeRuntimeTest.hasFeature("tools-sdk"):
        skipModule("Image doesn't have tools-sdk in IMAGE_FEATURES")


class CGLDummyTest1(oeRuntimeTest):

    @classmethod
    def setUpClass(self):
        oeRuntimeTest.tc.target.copy_to(os.path.join(oeRuntimeTest.tc.filesdir, "dummy_1.c"), "/tmp/dummy_1.c")

    def cgl_dummy_compile_test(self):
        (status, output) = self.target.run('gcc /tmp/dummy_1.c -o /tmp/dummy_1 -lm')
        self.assertEqual(status, 0, msg="gcc compile failed, output: %s" % output)
        (status, output) = self.target.run('/tmp/dummy_1')
        self.assertEqual(status, 0, msg="running compiled file failed, output %s" % output)

    @classmethod
    def tearDownClass(self):
        oeRuntimeTest.tc.target.run("rm /tmp/dummy_1.c /tmp/dummy_1.o /tmp/dummy_1")