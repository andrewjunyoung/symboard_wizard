"""
@author Andrew J. Young
@description Unit tests for the file test_states.py
"""


from unittest import main as unittest_main
from unittest import TestCase
from unittest.mock import mock_open, patch

# Imports from this package.
from symboard.states import load_yaml
from symboard.actions import State, latin


class TestStates(TestCase):
    def setUp(self):
        self.comma_separated_latin_lower = \
            'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'
        self.comma_separated_latin_upper = \
            self.comma_separated_latin_lower.upper()
        self.state_name = 'nothing'
        self.terminator = '.'

    def test_load_yaml_valid_input_without_upper(self):
        read_data = f'''
        {self.state_name}:
            terminator: {self.terminator}
            lower: {self.comma_separated_latin_lower}
        '''
        expected_states = {
            self.state_name: State(
                name=self.state_name,
                terminator=self.terminator
            ).with_lower(
                self.comma_separated_latin_lower
            )
        }

        with patch('builtins.open', mock_open(read_data=read_data)) as open_:
            actual_states = load_yaml()

        self.assertEqual(expected_states, actual_states)

    def test_load_yaml_valid_input_with_upper(self):
        read_data = f'''
        {self.state_name}:
            terminator: {self.terminator}
            lower: {self.comma_separated_latin_lower}
            upper: {self.comma_separated_latin_upper}
        '''
        expected_states = {
            self.state_name: State(
                name=self.state_name,
                terminator=self.terminator
            ).with_lower(
                self.comma_separated_latin_lower
            ).with_upper(
                self.comma_separated_latin_upper
            )
        }

        with patch('builtins.open', mock_open(read_data=read_data)) as open_:
            actual_states = load_yaml()

        self.assertEqual(expected_states, actual_states)

    # TODO: Test on invalid inputs

    def test_unicode_conversion_of_actions(self):
        apostrophe_output = 'apostrophe'
        read_data = f'''
        {self.state_name}:
            terminator: {self.terminator}
            map:
                "'": {apostrophe_output}
        '''
        expected_states = {
            self.state_name: State(
                name=self.state_name,
                terminator=self.terminator
            ).with_map(
                {"&#x0027;": apostrophe_output}
            )
        }

        with patch('builtins.open', mock_open(read_data=read_data)) as open_:
            actual_states = load_yaml()

        self.assertEqual(expected_states, actual_states)
        pass


if __name__ == '__main__':
    unittest_main

