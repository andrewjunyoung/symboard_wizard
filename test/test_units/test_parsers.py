'''
@author Andrew J. Young
@description Unit tests for the file main.py
'''

# Package internal imports
from symboard.parsers import YamlFileParser
from symboard.errors import ParserException

# Third party packages
from test.utils import PARSERS_PATH
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch, mock_open


class TestYamlFileParser(TestCase):
    def setUp(self):
        self.input_file_path = 'test.yaml'
        self.spec = {
            'lower': 'lower',
            'CAPS': 'CAPS',
            'Int': 1,
            'Bool': True,
        }
        self.lower_spec = {
            'lower': 'lower',
            'caps': 'caps',
            'int': 1,
            'bool': True,
        }

    def test__try_lower(self):
        test_inputs = ['lower', 'CAPS', 1, True]
        expected = ['lower', 'caps', 1, True]

        for i, input_ in enumerate(test_inputs):
            self.assertEqual(expected[i], YamlFileParser._try_lower(input_))

    def test__lower_dict(self):
        expected = self.lower_spec
        self.assertEqual(expected, YamlFileParser._lower_dict(self.spec))

    @patch(PARSERS_PATH + '.isfile')
    def test_parse_raises_error_if_not_isfile(self, mock_isfile):
        mock_isfile.return_value = False

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            with self.assertRaises(ParserException):
                results = YamlFileParser.parse('')

    @patch(PARSERS_PATH + '.isfile')
    def test_parse_raises_error_if_exception_occurs(self, mock_isfile):
        mock_isfile.side_effect = ParserException()

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            with self.assertRaises(ParserException):
                results = YamlFileParser.parse(object)

    @patch(PARSERS_PATH + '.isfile')
    def test_parse_opens_file_path(self, mock_isfile):
        mock_isfile.return_value = True

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            YamlFileParser.parse(self.input_file_path)

            open_.assert_called_once_with(self.input_file_path, 'r')

    @patch(PARSERS_PATH + '.safe_load')
    @patch(PARSERS_PATH + '.isfile')
    def test_parse_case_sensitive(self, mock_isfile, mock_safe_load):
        expected = self.spec

        mock_isfile.return_value = True
        mock_safe_load.return_value = self.spec

        with patch('builtins.open', mock_open(read_data='data')):
            # Call parse with case_sensitive = True
            actual = YamlFileParser.parse(self.input_file_path)

        self.assertEqual(expected, actual)


    @patch(PARSERS_PATH + '.safe_load')
    @patch(PARSERS_PATH + '.isfile')
    def test_parse_not_case_sensitive(self, mock_isfile, mock_safe_load):
        expected = self.lower_spec

        mock_isfile.return_value = True
        mock_safe_load.return_value = self.spec

        with patch('builtins.open', mock_open(read_data='data')):
            actual = YamlFileParser.parse(
                self.input_file_path,
                case_sensitive = False
            )

        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest_main()
