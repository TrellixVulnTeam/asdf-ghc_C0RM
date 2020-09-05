from lib.list_all import list_all
from unittest.mock import Mock

import unittest

class TestListAll(unittest.TestCase):
  def test_list_all(self):
    printer = Mock()
    list_all(printer)
    self.assertIn('8.10.1', printer.call_args.args[0])
