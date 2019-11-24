'''
@author Andrew J. Young
@description Unit tests for the file orchestrator.py
'''

# Package internal imports
from symboard.orchestrator import Orchestrator

# Third party packages
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch
import sys


#class TestMain(TestCase):
#    def test_get_parser_has_correct_args(self):
#        # Setup.
#        testargs = ['python', 'input', 'output']
#        with patch.object(sys, 'argv', testargs):
#            # Execution.
#            parser = get_parser()
#            args = parser.parse_args()
#
#            # Assertion.
#            self.assertEqual(args.input_file_path, ['input'])
#            self.assertEqual(args.output_file_path, ['output'])


if __name__ == '__main__':
    unittest_main()
