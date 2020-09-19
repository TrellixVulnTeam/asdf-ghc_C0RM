from lib.distro import get_distro

import unittest


class TestDistro(unittest.TestCase):
    def test_get_distro(self):
        distro = get_distro('darwin')
        self.assertEqual(distro, {'name': 'apple', 'version': 0.0})
