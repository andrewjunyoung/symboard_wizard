from unittest import main as unittest_main
from unittest import TestCase
from unittest.mock import patch

from symboard.errors import SpecificationException
from symboard.keylayouts.builders import (
    _class_from_base_keylayout,
    keylayout_from_spec,
)
from symboard.keylayouts.ansi_keylayout import AnsiKeylayout


BUILDERS_DIRECTORY = 'symboard.keylayouts.builders'


class TestBuilders(TestCase):
    def test__class_from_base_keylayout_raises_exception_when_fails(self):
        with self.assertRaises(SpecificationException):
            _class_from_base_keylayout(3)

    def test__class_from_base_keylayout_returns_instantiable_class(self):
        # Execution
        try:
            keylayout = _class_from_base_keylayout('ansi')(0, 0, 0)
            self.assertIsInstance(keylayout, AnsiKeylayout)
        except:
            # We should never reach here
            self.fail()

    @patch(BUILDERS_DIRECTORY + '._class_from_base_keylayout')
    def test_keylayout_from_spec_using_minimal_ansi_spec(
        self, mock__class_from_base_keylayout
    ):
        # Setup.
        mock__class_from_base_keylayout.return_value = AnsiKeylayout

        EXPECTED_DEFAULT_INDEX = 0
        EXPECTED_GROUP = 126
        EXPECTED_ID = -19234
        EXPECTED_MAXOUT = 1
        EXPECTED_NAME = 'Ansi keyboard'

        spec = {
            'base_layout': 'ansi',
            'id': EXPECTED_ID,
            'group': EXPECTED_GROUP,
        }


        # Execution.
        keylayout = keylayout_from_spec(spec)

        # Assertions.
        self.assertEqual(keylayout.default_index, EXPECTED_DEFAULT_INDEX)
        self.assertEqual(keylayout.group, EXPECTED_GROUP)
        self.assertEqual(keylayout.id_, EXPECTED_ID)
        self.assertEqual(keylayout.maxout, EXPECTED_MAXOUT)
        self.assertEqual(keylayout.name, EXPECTED_NAME)


    @patch(BUILDERS_DIRECTORY + '._class_from_base_keylayout')
    def test_keylayout_from_spec_using_full_spec(
        self, mock__class_from_base_keylayout
    ):
        # Setup.
        mock__class_from_base_keylayout.return_value = AnsiKeylayout

        EXPECTED_DEFAULT_INDEX = 3
        EXPECTED_GROUP = 101
        EXPECTED_ID = 101
        EXPECTED_MAXOUT = 3
        EXPECTED_NAME = 'Test ansi keylayout'

        spec = {
            'base_layout': 'ansi',
            'id': EXPECTED_ID,
            'group': EXPECTED_GROUP,
            'max_output_characters': EXPECTED_MAXOUT,
            'name': EXPECTED_NAME,
            'default_index': EXPECTED_DEFAULT_INDEX
        }

        # Execution.
        keylayout = keylayout_from_spec(spec)

        # Assertions.
        self.assertEqual(keylayout.default_index, EXPECTED_DEFAULT_INDEX)
        self.assertEqual(keylayout.group, EXPECTED_GROUP)
        self.assertEqual(keylayout.id_, EXPECTED_ID)
        self.assertEqual(keylayout.maxout, EXPECTED_MAXOUT)
        self.assertEqual(keylayout.name, EXPECTED_NAME)

    def test_keylayout_from_spec_raises_exception_when_fails(self):
        with self.assertRaises(SpecificationException):
            keylayout_from_spec({})


if __name__ == '__main__':
    unittest_main()

