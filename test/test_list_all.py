from lib.list_all import list_all

import unittest


class TestListAll(unittest.TestCase):
    def test_list_all(self):
        versions = list_all()
        self.assertIn('8.10.2', versions)
        self.assertIn('8.8.4', versions)
        self.assertIn('8.6.5', versions)
