from lib.install import main

import subprocess
import tempfile
import unittest


class TestInstall(unittest.TestCase):
    def test_install_8_10_2(self):
        with tempfile.TemporaryDirectory() as install_dir:
            main(install_dir, '8.10.2')
            output = subprocess.check_output(
                ['%s/bin/ghc' % install_dir, '--version']
            )
            self.assertIn(b'8.10.2', output)
