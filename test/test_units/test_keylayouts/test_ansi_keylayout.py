'''
@author: Andrew J. Young
@description: Acceptance tests for the ansi keyboard
'''


# Imports from third party packages
from unittest import TestCase
from unittest import main as unittest_main

# Package internal imports
from symboard.keylayouts.ansi_keylayout import AnsiKeylayout
from test.test_units.test_keylayouts.test_keylayouts import TestKeylayout


class TestAnsiKeylayout(TestKeylayout):
    def setUp(self):
        self.GROUP = 1
        self.ID = 2
        self.NAME = '3'
        self.MAXOUT = 4
        self.DEFAULT_INDEX = 5

        self.class_ = AnsiKeylayout
        self.keylayout = self.class_(
            self.GROUP,
            self.ID,
            name = self.NAME,
            maxout = self.MAXOUT,
            default_index = self.DEFAULT_INDEX,
        )

    def test_keylayout_str(self):
        expected = 'AnsiKeylayout({}, (id: {}))'.format(self.NAME, self.ID)
        actual = str(self.keylayout)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest_main()

