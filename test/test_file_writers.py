'''
@author Andrew J. Young
@description Unit tests for the file main.py
'''

# Package internal imports
from symboard.file_writers import KeylayoutFileWriter, DEFAULT_OUTPUT_FILE_PATH
from symboard.errors import WriteException

# Third party packages
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch, mock_open, MagicMock
import os.path


class TestKeylayoutFileWriter(TestCase):

    @patch('symboard.file_writers.exists')
    def test_write_opens_the_output_file_path(self, mock_exists):
        # Setup.
        output_file_path = 'test'
        mock_exists.return_value = False

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            KeylayoutFileWriter.write(output_file_path)

            open_.assert_called_once_with(output_file_path, 'w+')

    @patch('symboard.file_writers.exists')
    def test_write_throws_exception_if_the_file_exists(self, mock_exists):
        output_file_path = 'test'
        mock_exists.return_value = True

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            with self.assertRaises(WriteException):
                 KeylayoutFileWriter.write(output_file_path)


    @patch('symboard.file_writers.exists')
    def test_write_allows_for_no_arguments(self, mock_exists):
        open_ = mock_open()
        mock_exists.return_value = False

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            KeylayoutFileWriter.write()

        open_.assert_called_once_with(DEFAULT_OUTPUT_FILE_PATH, 'w+')


if __name__ == '__main__':
    unittest_main()
