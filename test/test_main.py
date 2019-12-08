'''
@author Andrew J. Young
@description Unit tests for the file main.py
'''

# Package internal imports
from symboard.main import main, get_arg_parser
from symboard.orchestrator import Orchestrator

# Third party packages
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch
import sys


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


if __name__ == '__main__':
    unittest_main()

