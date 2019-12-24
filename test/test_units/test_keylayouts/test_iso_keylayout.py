'''
@author: Andrew J. Young
@description: Acceptance tests for the iso_keyboard
'''

# Imports from third party packages
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch, Mock, MagicMock
from os import remove

# Package internal imports
from symboard.keylayouts.iso_keylayout import IsoKeylayout
from symboard.file_writers import KeylayoutXMLFileWriter
from test.test_keylayouts.test_keylayouts import TestKeylayout


file_writers_path = 'symboard.file_writers'


class TestIsoKeylayout(TestKeylayout):
    def setUp(self):
        self.GROUP = 1
        self.ID = 2
        self.NAME = '3'
        self.MAXOUT = 4
        self.DEFAULT_INDEX = 5

        self.class_ = IsoKeylayout
        self.keylayout = self.class_(
            self.GROUP,
            self.ID,
            name = self.NAME,
            maxout = self.MAXOUT,
            default_index = self.DEFAULT_INDEX,
        )

    def test_keylayout_str(self):
        expected = 'IsoKeylayout({}, (id: {}))'.format(self.NAME, self.ID)
        actual = str(self.keylayout)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest_main()

