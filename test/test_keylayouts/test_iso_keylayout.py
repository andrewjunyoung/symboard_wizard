'''
@author: Andrew J. Young
@description: Acceptance tests for the iso_keyboard
'''

# Imports from third party packages
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch, Mock, MagicMock
from os import remove

# Package internal imports
from symboard.keylayouts.iso_keylayout import IsoKeylayout
from symboard.file_writers import KeylayoutXMLFileWriter
from test.test_keylayouts.test_keylayouts import TestKeylayout


file_writers_path = 'symboard.file_writers'


class TestIsoKeylayout(TestKeylayout):
    def setUp(self):
        self.GROUP = 1
        self.ID = 2
        self.NAME = '3'
        self.MAXOUT = 4
        self.DEFAULT_INDEX = 5

        self.keylayout = IsoKeylayout(
            self.GROUP,
            self.ID,
            name = self.NAME,
            maxout = self.MAXOUT,
            default_index = self.DEFAULT_INDEX,
        )

    def test_keylayout_str(self):
        expected = 'IsoKeylayout({}, (id: {}))'.format(self.NAME, self.ID)
        actual = str(self.keylayout)

        self.assertEqual(expected, actual)


class TestIsoKeyboardIntegration(TestCase):
    def setUp(self):
        self.EXPECTED_ISO_KEYLAYOUT_PATH = 'test/res/' \
            'expected_iso_keylayout.keylayout'
        self.OUTPUT_PATH = 'actual'

        self.GROUP = 126
        self.ID = -19341
        self.DEFAULT_INDEX = 6

        self.iso_keylayout = IsoKeylayout(
            self.GROUP,
            self.ID,
            default_index = self.DEFAULT_INDEX
        )
        self.keylayout_xml_file_writer = KeylayoutXMLFileWriter()

        self.maxDiff = None

        self.mock = Mock()

    @patch(file_writers_path + '.datetime')
    def test_output_is_as_expected(self, datetime):
        '''
        !!! WARNING: This function *will* write to disk !!!
        '''
        # Setup.
        mock_datetime = self.mock
        datetime.now = MagicMock(return_value=mock_datetime)
        mock_datetime.strftime.return_value = '2019-12-07 21:54:51 (UTC)'

        # Execution.
        self.keylayout_xml_file_writer.write(
            self.iso_keylayout, self.OUTPUT_PATH
        )

        try:
            with open(self.OUTPUT_PATH + '.keylayout', 'r') as file_:
                actual = file_.read()
            remove(self.OUTPUT_PATH + '.keylayout')
        except:
            remove(self.OUTPUT_PATH + '.keylayout')
            self.fail() # We should never get here.


        with open(self.EXPECTED_ISO_KEYLAYOUT_PATH, 'r') as file_:
            expected = file_.read()

        # Assertion.
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest_main()
