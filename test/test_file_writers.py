'''
@author Andrew J. Young
@description Unit tests for the file main.py
'''

# Package internal imports
from symboard.file_writers import (
    FileWriter,
    KeylayoutFileWriter,
    DEFAULT_OUTPUT_PATH,
)
from symboard.errors import WriteException

# Imports from third party packages.
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch, mock_open, MagicMock
import os.path


class TestFileWriter(TestCase):
    def setUp(self):
        self.file_writer = FileWriter()
        self.test_prefix = './hello/file'
        self.test_postfix = 'keylayout'

    def test_change_postfix_adds_postfix_when_no_match(self):
        test_path = self.test_prefix
        expected = self.test_prefix + '.' + self.test_postfix

        actual = self.file_writer.change_postfix(test_path, self.test_postfix)

        self.assertEqual(expected, actual)

    def test_change_postfix_corrects_incorrect_postfix(self):
        test_path = self.test_prefix + '.wrong_postfix'
        expected = self.test_prefix + '.' + self.test_postfix

        actual = self.file_writer.change_postfix(test_path, self.test_postfix)

        self.assertEqual(expected, actual)

    def test_change_postfix_does_nothing_when_correct_postfix(self):
        test_path = self.test_prefix + '.' + self.test_postfix
        expected = test_path

        actual = self.file_writer.change_postfix(test_path, self.test_postfix)

        self.assertEqual(expected, actual)

class TestKeylayoutFileWriter(TestCase):
    def setUp(self):
        self.keylayout_file_writer = KeylayoutFileWriter()

    @patch('symboard.file_writers.exists')
    def test_write_opens_the_output_file_path(self, mock_exists):
        # Setup.
        output_file_path = 'test'
        mock_exists.return_value = False

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            self.keylayout_file_writer.write(None, output_file_path)

            open_.assert_called_once_with(output_file_path, 'w+')

    @patch('symboard.file_writers.exists')
    def test_write_throws_exception_if_the_file_exists(self, mock_exists):
        output_file_path = 'test'
        mock_exists.return_value = True

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            with self.assertRaises(WriteException):
                 self.keylayout_file_writer.write(None, output_file_path)


    @patch('symboard.file_writers.exists')
    def test_write_allows_for_no_arguments(self, mock_exists):
        open_ = mock_open()
        mock_exists.return_value = False

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            self.keylayout_file_writer.write(None)

        open_.assert_called_once_with(DEFAULT_OUTPUT_PATH, 'w+')


if __name__ == '__main__':
    unittest_main()
