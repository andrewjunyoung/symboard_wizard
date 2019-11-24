'''
@author Andrew J. Young
@description Unit tests for the file main.py
'''

# Package internal imports
from symboard.main import main, get_parser
from symboard.orchestrator import Orchestrator

# Third party packages
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch
import sys


#class TestMain(TestCase):
#    def test_get_parser_raises_error():
#        input_file_path = 'test.yml'
#        open_ = mock_open()
#
#        with self.assertRaises(ParserError):
#            with patch('__main__.open', open_):
#                results = YamlFileParser.parse('')
#
#    def test_get_parser_does_not_raise_error():
#        input_file_path = 'test.yml'
#        open_ = mock_open()
#
#        with self.assertRaises(ParserError):
#            with patch('__main__.open', open_):
#                results = YamlFileParser.parse('test.yml')
#
#if __name__ == '__main__':
#    unittest_main()
