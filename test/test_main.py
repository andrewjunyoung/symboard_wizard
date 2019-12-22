'''
@author Andrew J. Young
@description Unit tests for the file main.py
'''


# Imports from third party packages.
from os import remove
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch, Mock, MagicMock
import sys

# Package internal imports
from symboard.main import main, get_arg_parser
from symboard.orchestrator import Orchestrator


class TestMain(TestCase):
    def test_get_arg_parser_has_correct_args(self):
        # Setup.
        testargs = ['python', 'input', 'output']
        with patch.object(sys, 'argv', testargs):
            # Execution.
            parser = get_arg_parser()
            args = parser.parse_args()

            # Assertion.
            self.assertEqual(args.input_file_path, ['input'])
            self.assertEqual(args.output_file_path, ['output'])


class TestMainIntegration(TestCase):
    def setUp(self):
        self.orchestrator = Orchestrator()
        self.OUTPUT_PATH = 'output2'
        self.INPUT_PATH = 'test/res/minimal_input_ansi.yaml'
        self.EXPECTED_ANSI_KEYLAYOUT_PATH = 'test/res/' \
            'expected_ansi_keylayout.keylayout'

    @patch('symboard.file_writers.datetime')
    def test_integration_with_minimal_ansi_input_yaml(self, datetime):
        '''
        !!! WARNING: This function *will* write to disk !!!
        '''
        # Setup.
        mock_datetime = Mock()
        datetime.now = MagicMock(return_value = mock_datetime)
        mock_datetime.strftime.return_value = '2019-12-07 21:54:51 (UTC)'

        # Execution.
        self.orchestrator.run(self.INPUT_PATH, self.OUTPUT_PATH)

        try:
            with open(self.OUTPUT_PATH + '.keylayout', 'r') as file_:
                actual = file_.read()
            remove(self.OUTPUT_PATH + '.keylayout')
        except:
            remove(self.OUTPUT_PATH + '.keylayout')
            self.fail() # We should never get here.

        with open(self.EXPECTED_ANSI_KEYLAYOUT_PATH, 'r') as file_:
            expected = file_.read()

        # Assertion.
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest_main()

