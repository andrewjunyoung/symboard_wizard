'''
@author: Andrew J. Young
@description: Integration tests for the keylayouts supported by symboard.
'''

# Imports from third party packages.
from unittest import TestCase, skip
from unittest.mock import patch, Mock, MagicMock
from unittest import main as unittest_main
from os import remove, getenv
import logging

# Imports from the local package.
from test.utils import FILE_WRITERS_PATH, RES_DIR
from symboard.file_writers import KeylayoutXMLFileWriter
from symboard.states import load_yaml
from symboard.keylayout import KeylayoutFactory


DEFAULT_FILE_DELETION_ENV_VAR = 'KEEP_INTEGRATION_TEST_OUTPUT_FILE'
OVERWRITE_TEST_OUTPUT_FILES = 'OVERWRITE_TEST_OUTPUT_FILES'

keylayout_factory = KeylayoutFactory()


class KeyboardIntegrationTests:
    class IntegrationTest(TestCase):
        def _setUp(
            self, base_layout, id_ = -19341, DEFAULT_INDEX = 6,
            FILE_DELETION_ENV_VAR = DEFAULT_FILE_DELETION_ENV_VAR,
        ):
            self.EXPECTED_OUTPUT_PATH = f'{RES_DIR}{base_layout}.keylayout'
            self.ACTUAL_OUTPUT_PATH = 'actual' + str(self.__class__.__name__) \
                + '.keylayout'

            self.GROUP = 126
            self.ID = id_
            self.DEFAULT_INDEX = DEFAULT_INDEX

            self.keylayout = keylayout_factory.from_spec({
                'base_layout': base_layout,
                'group': self.GROUP,
                'id': self.ID,
                'default_index': self.DEFAULT_INDEX,
            })
            self.keylayout_xml_file_writer = KeylayoutXMLFileWriter()

            self.maxDiff = 1000

            self.OVERWRITE_OUTPUT = getenv(OVERWRITE_TEST_OUTPUT_FILES)

            if getenv(FILE_DELETION_ENV_VAR):
                self.KEEP_FILE = getenv(FILE_DELETION_ENV_VAR)
            elif getenv(DEFAULT_FILE_DELETION_ENV_VAR):
                self.KEEP_FILE = getenv(DEFAULT_FILE_DELETION_ENV_VAR)
            else:
                logging.warning(
                    f'Failed to find file deletion environment variable at '
                    f'{FILE_DELETION_ENV_VAR} and '
                    f'{DEFAULT_FILE_DELETION_ENV_VAR}. Setting KEEP_FILE = '
                    f'False.'
                )
                self.KEEP_FILE = False

            self.states = load_yaml()

        def setUp(self):
            # This should be implemented by children which inherit from this class.
            pass

        # For some reason, this works with bools, but not objects.
        @patch(FILE_WRITERS_PATH + '.OVERWRITE_OUTPUT', True)
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
            'iso',
            FILE_DELETION_ENV_VAR='KEEP_ISO_INTEGRATION_TEST_OUTPUT_FILE',
        )


class TestIsoDvorakKeyboardIntegration(KeyboardIntegrationTests.IntegrationTest):
    def setUp(self):
        self._setUp(
            'iso_dvorak',
            id_ = -5586,
            FILE_DELETION_ENV_VAR='KEEP_ISO_DVORAK_INTEGRATION_TEST_OUTPUT_FILE',
        )

@skip('Todo: migrate iso JDvorak to yaml.')
class TestIsoJDvorakKeyboardIntegration(KeyboardIntegrationTests.IntegrationTest):
    def setUp(self):
        self._setUp(
            'iso_jdvorak',
            id_  = -31708,
            DEFAULT_INDEX = 4,
            FILE_DELETION_ENV_VAR='KEEP_ISO_JDVORAK_INTEGRATION_TEST_OUTPUT_FILE',
        )


if __name__ == '__main__':
    unittest_main()

