from lib.distro import get_distro

import sys
import unittest


class TestDistro(unittest.TestCase):
    def test_get_distro_darwin(self):
        distro = get_distro('darwin')
        self.assertEqual(distro, {'name': 'apple', 'version': 0.0})

    @unittest.skipUnless(sys.platform == 'linux', 'requires linux')
    def test_get_distro_linux(self):
        distro = get_distro('linux')
        self.assertEqual(distro, {'name': 'deb', 'version': 10.0})
