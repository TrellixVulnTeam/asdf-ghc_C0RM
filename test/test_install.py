import lib.install
import subprocess
import tempfile
import unittest

class TestInstall(unittest.TestCase):
    def test_install(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bin_dir = lib.install.install(tmpdir, '8.8.1')
            version = subprocess.check_output([f"{bin_dir}/ghc", '--version'])
            self.assertIn(b'8.8.1', version)
