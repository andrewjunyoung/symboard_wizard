'''
@author: Andrew J. Young
@description: Acceptance tests for the ansi_keyboard
'''

# Third party imports
from unittest import TestCase
from unittest import main as unittest_main

# Package internal imports
from symboard.keylayouts.ansi_keylayout import AnsiKeylayout

class TestAnsiKeylayout(TestCase):
    def setUp(self):
        self.ansi_keylayout = AnsiKeylayout()

    def test_default_name_is_ansi_keyboard(self):
        self.assertEqual(self.ansi_keylayout.name, AnsiKeylayout.DEFAULT_NAME)

    def test_name_overwrite(self):
        TEST_NAME = 'test_name'
        ansi_keylayout = AnsiKeylayout(TEST_NAME)

        self.assertEqual(ansi_keylayout.name, TEST_NAME)

    def test_output_is_as_expected(self):
        self.ansi_keylayout.write(self.OUTPUT_PATH)

        with open(self.ansi_keylayout_expected.keylayout, 'r') as file_:
            expected = file_.read()
        with open(self.OUTPUT_PATH, 'r') as file_:
            actual = file_.read()

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest_main()
