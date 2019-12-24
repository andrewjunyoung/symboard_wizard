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
from test.utils import RES_DIR
from symboard.main import get_arg_parser

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

