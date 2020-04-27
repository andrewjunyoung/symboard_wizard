"""
.. module:: actions
   :synopsis: The functionality required to include actions and states for
   keyboards.

.. moduleauthor:: Andrew J. Young
"""


# Imports from third party packages.
from yaml import safe_load
from dataclasses import dataclass

# Imports from the local package.
from symboard.errors import AlphabetLengthException


states_list: set = set()
actions_list: set = set()


# TODO: Standardize
with open('symboard/alphabets.yaml', 'r') as file_:
    alphabets = safe_load(file_)
latin_alphabet_lower = alphabets['latin_lower']


@dataclass(init=True, eq=True, repr=True, order=True, frozen=True)
class Action:
    id_: str = None


@dataclass(init=True, eq=True, repr=True)
class State:
    name: str = None
    terminator: str = None
    action_to_output_map: dict = None

    def with_alphabet(self, output_lower: str) -> None:
        # TODO: Write tests

        if len(output_lower) != 26:
            raise AlphabetLengthException(len(output_lower))

        self.action_to_output_map = {
            latin_alphabet_lower[i]: output_lower[i]
            for i in range(len(output_lower))
        }
