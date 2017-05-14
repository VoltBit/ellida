import unittest
import os
from oeqa.oetest import oeRuntimeTest, skipModule
from oeqa.utils.decorators import *

def setUpModule():
    if not oeRuntimeTest.hasFeature("tools-sdk"):
        skipModule("Image doesn't have tools-sdk in IMAGE_FEATURES")
    if not oeRuntimeTest.hasPackage("rust"):
        skipModule("Image doesn't have rust installed")
    if not oeRuntimeTest.hasPackage("cargo"):
        skipModule("Image doesn't have cargo installed")

class CGLDummyTest2(oeRuntimeTest):

    @classmethod
    def setUpClass(self):
        oeRuntimeTest.tc.target.copy_to(os.path.join(oeRuntimeTest.tc.filesdir, "dummy_2"), "/tmp/dummy_2")
        oeRuntimeTest.tc.target.run('cd /tmp')
        oeRuntimeTest.tc.target.run('cargo new dummy2 --bin')

    def cgl_dummy_compile_test(self):
        (status, output) = self.target.run('cargo build -q /tmp/dummy2')
        self.assertEqual(status, 0, msg="rust compile failed, output: %s" % output)
        (status, output) = self.target.run('cargo run -q /tmp/dummy2')
        self.assertEqual(status, 0, msg="running run file failed, output %s" % output)

    @classmethod
    def tearDownClass(self):
        oeRuntimeTest.tc.target.run('rm -rf /tmp/dummy2')