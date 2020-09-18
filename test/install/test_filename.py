from lib.install.filename import parse_filename

import unittest


class TestFilename(unittest.TestCase):
    def test_parse_filename_apple(self):
        value = parse_filename('ghc-8.10.2-x86_64-apple-darwin.tar.xz')
        self.assertEqual(value, {
            'filename': 'ghc-8.10.2-x86_64-apple-darwin.tar.xz',
            'distro': {
                'name': 'apple',
                'version': 0
            },
            'extras': []
        })

    def test_parse_filename_centos(self):
        value = parse_filename('ghc-8.10.2-x86_64-centos7-linux.tar.xz')
        self.assertEqual(value, {
            'filename': 'ghc-8.10.2-x86_64-centos7-linux.tar.xz',
            'distro': {
                'name': 'centos',
                'version': 7.0
            },
            'extras': []
        })

    def test_parse_filename_deb(self):
        value = parse_filename('ghc-8.10.2-x86_64-deb10-linux.tar.xz')
        self.assertEqual(value, {
            'filename': 'ghc-8.10.2-x86_64-deb10-linux.tar.xz',
            'distro': {
                'name': 'deb',
                'version': 10.0
            },
            'extras': []
        })
