from lib.list_all import list_all
from unittest.mock import Mock

import unittest


class TestListAll(unittest.TestCase):
    def test_list_all(self):
        printer = Mock()
        list_all(printer)
        versions = printer.call_args.args[0]
        self.assertIn('8.10.2', versions)
        self.assertIn('8.8.4', versions)
        self.assertIn('8.6.5', versions)
