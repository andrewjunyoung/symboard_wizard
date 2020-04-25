from symboard.actions import State
from unittest import TestCase
from unittest import main as unittest_main





class TestState(TestCase):
    def _test_with_alphabet_asserts_length(self, alphabet):
        with self.assertRaises(AlphabetLengthError):
            self.state.with_alphabet(alphabet)

    def test_with_alphabet_assert_length(self):
        test_state = State('acute', terminator = '´')
        inputs = [
            '',
            '1',
            'pyfgcrlaoeuidhtnsqjkxbmwvz',
            'abcdefghijklmnopqrstuvwxyz',
            '1234567890123456789012345',
            '123456789012345678901234567',
            None,
            3,
        ]

        for input_ in inputs:
            self._test_with_alphabet_asserts_length(input_)

    #@patch(actions_path + '.latin_alphabet_lower')
    #def test_with_alphabet_sets_action_to_output_map(self):
    #    test_state = State('acute', terminator = '´')
    #    expected_action_to_output_map = {
    #        'key': 'value'
    #    }
    #    latin_


if __name__ == '__main__':
    unittest_main()
