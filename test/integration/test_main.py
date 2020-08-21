'''
@author: Andrew J. Young
@description: Integration tests for the main module of symboard.
'''


from os import remove

# Imports from the local package.
from test.utils import RES_DIR
from symboard import main
from symboard.main import main, get_arg_parser
from symboard.orchestrator import Orchestrator
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch, Mock, MagicMock


class TestMainIntegration(TestCase):
    def setUp(self):
        self.orchestrator = Orchestrator()
        self.OUTPUT_PATH = 'output2'
        self.INPUT_PATH = RES_DIR + 'minimal_iso.yaml'
        self.EXPECTED_ANSI_KEYLAYOUT_PATH = RES_DIR \
            + 'iso.keylayout'

        self.maxDiff = None

    @patch('symboard.file_writers.VERSION', '0.2.0')
    @patch('symboard.file_writers.datetime')
    def test_integration_with_minimal_iso_yaml(self, datetime):
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
