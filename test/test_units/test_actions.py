# Imports from third party packages.
from unittest import TestCase
from unittest import main as unittest_main

# Imports from the local package.
from symboard.actions import State
from symboard.errors import AlphabetLengthException


class TestState(TestCase):
    def test_with_lower_raises_exception_when_not_valid_length(self):
        state = State(name='acute', terminator='´')
        inputs = [
            '',
            '1',
            '1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5',  # Length 25
            '1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7',  # Length 27
            '1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,' \
                '1,2,3,4,5',  # Length 35
            '1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,' \
                '1,2,3,4,5,6,7',  # Length 37
        ]

        for input_ in inputs:
            with self.assertRaises(AlphabetLengthException):
                state.with_lower(input_)

    def test_with_lower_does_not_raise_exception_when_length_26(self):
        state = State(name='acute', terminator='´')
        inputs = [
            'p,y,f,g,c,r,l,a,o,e,u,i,d,h,t,n,s,q,j,k,x,b,m,w,v,z',
            'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z',
        ]

        for input_ in inputs:
            state.with_lower(input_)

    # TODO: Test _get_actions


if __name__ == '__main__':
    unittest_main()
