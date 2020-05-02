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
    def test_load_yaml_valid_input(self):
        state_name = 'nothing'
        comma_separated_latin_lower = \
            'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'
        read_data = f'''
        {state_name}:
            terminator: .
            lower: {comma_separated_latin_lower}
            upper: A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z
        '''
        expected_states = {
            state_name: State(name=state_name, terminator='.').with_lower(
                comma_separated_latin_lower
            )
        }

        with patch('builtins.open', mock_open(read_data=read_data)) as open_:
            actual_states = load_yaml()

        self.assertEqual(expected_states, actual_states)

    # TODO: Test on invalid inputs


if __name__ == '__main__':
    unittest_main

