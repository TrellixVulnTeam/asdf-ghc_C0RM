from lib.install import install

import subprocess
import tempfile
import unittest

class TestInstall(unittest.TestCase):
  def test_install_8_10_1(self):
    with tempfile.TemporaryDirectory() as install_dir:
      install(install_dir, '8.10.1')
      output = subprocess.check_output([f'{install_dir}/bin/ghc', '--version'])
      self.assertIn(b'8.10.1', output)

  def test_install_8_6_5(self):
    with tempfile.TemporaryDirectory() as install_dir:
      install(install_dir, '8.6.5')
      output = subprocess.check_output([f'{install_dir}/bin/ghc', '--version'])
      self.assertIn(b'8.6.5', output)
