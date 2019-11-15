import io
import lib.list_all
import unittest
import unittest.mock

class TestListAll(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_list_all(self, mock_stdout):
        lib.list_all.list_all()
        versions = mock_stdout.getvalue().split()
        self.assertIn('8.8.1', versions)

    def test_list_versions(self):
        versions = lib.list_all.list_versions()
        self.assertIn('8.8.1', versions)
