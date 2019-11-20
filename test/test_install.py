import lib.install
import subprocess
import tempfile
import unittest

class TestInstall(unittest.TestCase):
    # def test_install(self):
        # with tempfile.TemporaryDirectory() as tmpdir:
            # bin_dir = lib.install.install(tmpdir, '8.8.1')
            # version = subprocess.check_output([f"{bin_dir}/ghc", '--version'])
            # self.assertIn(b'8.8.1', version)
    def test_assets_urls(self):
        url = 'https://downloads.haskell.org/~ghc/8.8.1'
        urls = list(lib.install.assets_urls('8.8.1', 'linux', 'x86_64'))
        self.assertEqual(urls, [
            (f"{url}/ghc-8.8.1-x86_64-centos7-linux.tar.xz", ['centos7']),
            (f"{url}/ghc-8.8.1-x86_64-deb8-linux.tar.xz", ['deb8']),
            (f"{url}/ghc-8.8.1-x86_64-deb9-linux-dwarf.tar.xz", ['deb9', 'dwarf']),
            (f"{url}/ghc-8.8.1-x86_64-deb9-linux.tar.xz", ['deb9']),
            (f"{url}/ghc-8.8.1-x86_64-fedora27-linux.tar.xz", ['fedora27'])
        ])
