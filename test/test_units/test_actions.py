# Imports from third party packages.
from unittest import TestCase
from unittest import main as unittest_main

# Imports from the local package.
from symboard.actions import State
from symboard.errors import AlphabetLengthException



class TestState(TestCase):
    def test_with_alphabet_raises_exception_when_not_length_26(self):
        state = State('acute', terminator = '´')
        inputs = [
            '',
            '1',
            '1234567890123456789012345',
            '123456789012345678901234567',
        ]

        for input_ in inputs:
            with self.assertRaises(AlphabetLengthException):
                state.with_alphabet(input_)

    def test_with_alphabet_does_not_raise_exception_when_length_26(self):
        state = State('acute', terminator = '´')
        inputs = [
            'pyfgcrlaoeuidhtnsqjkxbmwvz',
            'abcdefghijklmnopqrstuvwxyz',
        ]

        for input_ in inputs:
            state.with_alphabet(input_)

    #@patch(actions_path + '.latin_alphabet_lower')
    #def test_with_alphabet_sets_action_to_output_map(self):
    #    test_state = State('acute', terminator = '´')
    #    expected_action_to_output_map = {
    #        'key': 'value'
    #    }
    #    latin_


if __name__ == '__main__':
    unittest_main()
