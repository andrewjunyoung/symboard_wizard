"""
.. module:: actions
   :synopsis: The functionality required to include actions and states for
   keyboards.

.. moduleauthor:: Andrew J. Young
"""


from yaml import safe_load
from dataclasses import dataclass


states_list: set = set()
actions_list: set = set()


# TODO: Standardize
with open('symboard/alphabets.yaml', 'r') as file_:
    alphabets = safe_load(file_)
latin_alphabet_lower = alphabets['latin_lower']


@dataclass(init=True, eq=True, repr=True)
class Action:
    id_: str = None


@dataclass(init=True, eq=True, repr=True)
class State:
    name: str = None
    terminator: str = None
    action_to_output_map: dict = {}

    def with_alphabet(output_lower: str) -> None:
        # TODO: Write tests

        if len(alphabet) != 26:
            return AlphabetLengthError(len(alphabet))

        self.action_to_output_map = {
            latin_alphabet_lower[i]: output_lower[i]
        }

acute_state = State('acute', terminator='α').with_keylayout(
    output_lower='áb́ćd́éf́ǵh́íȷ́ḱĺḿńóṕq́ŕśt́úv́ẃx́ýź',
)
