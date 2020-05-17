'''
@author: Andrew J. Young
@description: Integratino tests for the keylayouts supported by symboard.
'''

# Imports from third party packages.
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock
from unittest import main as unittest_main
from os import remove, getenv

# Imports from the local package.
from test.utils import FILE_WRITERS_PATH, RES_DIR
from symboard.keylayouts.iso_keylayout import IsoKeylayout
from symboard.keylayouts.iso_dvorak_keylayout import IsoDvorakKeylayout
from symboard.keylayouts.iso_jdvorak_keylayout import IsoJDvorakKeylayout
from symboard.file_writers import KeylayoutXMLFileWriter
from symboard.states import load_yaml


DEFAULT_FILE_DELETION_ENV_VAR = 'KEEP_INTEGRATION_TEST_OUTPUT_FILE'


class KeyboardIntegrationTests:
    class IntegrationTest(TestCase):
        def _setUp(
            self, EXPECTED_OUTPUT_PATH, class_, id_ = -19341, DEFAULT_INDEX = 6,
            FILE_DELETION_ENV_VAR = DEFAULT_FILE_DELETION_ENV_VAR,
        ):
            self.EXPECTED_OUTPUT_PATH = EXPECTED_OUTPUT_PATH
            self.ACTUAL_OUTPUT_PATH = 'actual' + str(self.__class__.__name__) \
                + '.keylayout'

            self.GROUP = 126
            self.ID = id_
            self.DEFAULT_INDEX = DEFAULT_INDEX

            self.class_ = class_
            self.keylayout = self.class_(
                self.GROUP,
                self.ID,
                default_index = self.DEFAULT_INDEX,
            )
            self.keylayout_xml_file_writer = KeylayoutXMLFileWriter()

            self.maxDiff = 1000

            self.mock = Mock()

            if getenv(FILE_DELETION_ENV_VAR):
                self.KEEP_FILE = getenv(FILE_DELETION_ENV_VAR)
            elif getenv(DEFAULT_FILE_DELETION_ENV_VAR):
                self.KEEP_FILE = getenv(DEFAULT_FILE_DELETION_ENV_VAR)
            else:
                # TODO: Log an exception
                self.KEEP_FILE = False

            self.states = load_yaml()

        def setUp(self):
            # This should be implemented by children which inherit from this class.
            pass

        @patch(FILE_WRITERS_PATH + '.VERSION', '0.2.0')
        @patch(FILE_WRITERS_PATH + '.datetime')
        def test_output_is_as_expected(self, datetime):
            '''
            !!! WARNING: This function *will* write to disk !!!
            '''
            # Setup.
            OUTPUT_PATH = self.ACTUAL_OUTPUT_PATH

            mock_datetime = Mock()
            mock_datetime.strftime.return_value = '2019-12-07 21:54:51 (UTC)'
            datetime.now = MagicMock(return_value=mock_datetime)

            self.keylayout.create_used_states(self.states)

            # Execution.
            self.keylayout_xml_file_writer.write(
                self.keylayout, OUTPUT_PATH
            )

            try:
                with open(OUTPUT_PATH, 'r') as file_:
                    actual = file_.read()
                if not self.KEEP_FILE:
                    remove(OUTPUT_PATH)
            except:
                if not self.KEEP_FILE:
                    remove(OUTPUT_PATH)
                self.fail()  # We should never get here.

            with open(self.EXPECTED_OUTPUT_PATH, 'r') as file_:
                expected = file_.read()

            # Assertion.
            # Optimization for the strings not being equal.
            self.assertEqual(len(expected), len(actual))
            self.assertEqual(expected, actual)


class TestIsoKeyboardIntegration(KeyboardIntegrationTests.IntegrationTest):
    def setUp(self):
        self._setUp(
            RES_DIR + 'iso.keylayout',
            IsoKeylayout,
            FILE_DELETION_ENV_VAR='KEEP_ISO_INTEGRATION_TEST_OUTPUT_FILE',
        )


class TestIsoDvorakKeyboardIntegration(KeyboardIntegrationTests.IntegrationTest):
    def setUp(self):
        self._setUp(
            RES_DIR + 'iso_dvorak.keylayout',
            IsoDvorakKeylayout,
            id_ = -5586,
            FILE_DELETION_ENV_VAR='KEEP_ISO_DVORAK_INTEGRATION_TEST_OUTPUT_FILE',
        )

class TestIsoJDvorakKeyboardIntegration(KeyboardIntegrationTests.IntegrationTest):
    def setUp(self):
        self._setUp(
            RES_DIR + 'iso_jdvorak.keylayout',
            IsoJDvorakKeylayout,
            id_  = -31708,
            DEFAULT_INDEX = 4,
            FILE_DELETION_ENV_VAR='KEEP_ISO_JDVORAK_INTEGRATION_TEST_OUTPUT_FILE',
        )


if __name__ == '__main__':
    unittest_main()

