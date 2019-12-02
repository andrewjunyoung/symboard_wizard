'''
@author: Andrew J. Young
@description: Acceptance tests for the ansi_keyboard
'''

# Third party imports
from unittest import TestCase
from unittest import main as unittest_main

# Package internal imports
from symboard.keylayouts.ansi_keylayout import AnsiKeylayout
from symboard.file_writers import KeylayoutXMLFileWriter
from test.test_keylayouts.test_keylayouts import TestKeylayout

class TestAnsiKeylayout(TestKeylayout):
    def setUp(self):
        self.GROUP = 1
        self.ID = 2
        self.MAXOUT = 3
        self.NAME = '4'
        self.DEFAULT_INDEX = 5

        self.keylayout = AnsiKeylayout(
            self.GROUP,
            self.ID,
            self.MAXOUT,
            name = self.NAME,
            default_index = self.DEFAULT_INDEX
        )

    def test_keylayout_str(self):
        expected = 'AnsiKeylayout({}, (id: {}))'.format(self.NAME, self.ID)
        actual = str(self.keylayout)

        self.assertEqual(expected, actual)


class TestAnsiKeyboardIntegration(TestCase):
    def setUp(self):
        self.EXPECTED_ANSI_KEYLAYOUT_PATH = 'test/res/' \
                'expected_ansi_keylayout.keylayout'
        self.OUTPUT_PATH = 'test'

        self.GROUP = 1
        self.ID = 2
        self.MAXOUT = 3
        self.NAME = '4'
        self.DEFAULT_INDEX = 5

        self.ansi_keylayout = AnsiKeylayout(
            self.GROUP,
            self.ID,
            self.MAXOUT,
            name = self.NAME,
            default_index = self.DEFAULT_INDEX
        )
        self.keylayout_xml_file_writer = KeylayoutXMLFileWriter()

    def test_output_is_as_expected(self):
        self.keylayout_xml_file_writer.write(self.ansi_keylayout, self.OUTPUT_PATH)

        with open(self.EXPECTED_ANSI_KEYLAYOUT_PATH, 'r') as file_:
            expected = file_.read()
        with open(self.OUTPUT_PATH, 'r') as file_:
            actual = file_.read()

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest_main()

