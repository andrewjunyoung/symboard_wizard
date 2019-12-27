'''
@author: Andrew J. Young
@description: Integratino tests for the keylayouts supported by symboard.
'''

# Imports from third party packages.
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock
from unittest import main as unittest_main
from os import remove

# Imports from the local package.
from test.utils import FILE_WRITERS_PATH, RES_DIR
from symboard.keylayouts.iso_keylayout import IsoKeylayout
from symboard.keylayouts.iso_dvorak_keylayout import IsoDvorakKeylayout
from symboard.file_writers import KeylayoutXMLFileWriter


class KeyboardIntegrationTests:

    class IntegrationTest(TestCase):
        def _setUp(self, EXPECTED_OUTPUT_PATH, class_, id_ = -19341):
            self.EXPECTED_OUTPUT_PATH = EXPECTED_OUTPUT_PATH
            self.ACTUAL_OUTPUT_PATH = 'actual'

            self.GROUP = 126
            self.ID = id_
            self.DEFAULT_INDEX = 6

            self.class_ = class_
            self.keylayout = self.class_(
                self.GROUP,
                self.ID,
                default_index = self.DEFAULT_INDEX,
            )
            self.keylayout_xml_file_writer = KeylayoutXMLFileWriter()

            self.maxDiff = None

            self.mock = Mock()

        def setUp(self):
            # This should be implemented by children which inherit from this class.
            pass

        @patch(FILE_WRITERS_PATH + '.datetime')
        def test_output_is_as_expected(self, datetime):
            '''
            !!! WARNING: This function *will* write to disk !!!
            '''
            # Setup.
            OUTPUT_PATH = self.ACTUAL_OUTPUT_PATH + '.keylayout'

            mock_datetime = self.mock
            datetime.now = MagicMock(return_value=mock_datetime)
            mock_datetime.strftime.return_value = '2019-12-07 21:54:51 (UTC)'

            # Execution.
            self.keylayout_xml_file_writer.write(
                self.keylayout, OUTPUT_PATH
            )

            try:
                with open(OUTPUT_PATH, 'r') as file_:
                    actual = file_.read()
                remove(OUTPUT_PATH)
            except:
                remove(OUTPUT_PATH)
                self.fail() # We should never get here.


            with open(self.EXPECTED_OUTPUT_PATH, 'r') as file_:
                expected = file_.read()

            # Assertion.
            self.assertEqual(expected, actual)


class TestIsoKeyboardIntegration(KeyboardIntegrationTests.IntegrationTest):
    def setUp(self):
        self._setUp(RES_DIR + 'expected_iso_keylayout.keylayout', IsoKeylayout)


class TestIsoDvorakKeyboardIntegration(KeyboardIntegrationTests.IntegrationTest):
    def setUp(self):
        self._setUp(
            RES_DIR + 'expected_iso_dvorak_keylayout.keylayout',
            IsoDvorakKeylayout,
            id_ = -5586,
        )


if __name__ == '__main__':
    unittest_main()

