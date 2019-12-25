'''
@author Andrew J. Young
@description Unit tests for the file main.py
'''

# Package internal imports
from symboard.parsers import YamlFileParser
from symboard.errors import ParserException

# Third party packages
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch, mock_open


class TestMain(TestCase):

    @patch('symboard.parsers.isfile')
    def test_get_parser_raises_error_if_not_isfile(self, mock_isfile):
        mock_isfile.return_value = False

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            with self.assertRaises(ParserException):
                results = YamlFileParser.parse('')

    @patch('symboard.parsers.isfile')
    def test_get_parser_raises_error_if_exception_occurs(self, mock_isfile):
        mock_isfile.side_effect = ParserException()

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            with self.assertRaises(ParserException):
                results = YamlFileParser.parse(object)

    @patch('symboard.parsers.isfile')
    def test_get_parser_opens_file_path(self, mock_isfile):
        input_file_path = 'test.yml'
        mock_isfile.return_value = True

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            YamlFileParser.parse(input_file_path)

            open_.assert_called_once_with(input_file_path, 'r')


if __name__ == '__main__':
    unittest_main()
