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


@dataclass(init=False, eq=True, repr=True)
class State:
    name: str = None
    terminator: str = None
    action_to_output_map: dict = None  # TODO: fix

    def __init__(self, name, terminator, action_to_output_map=None):
        self.name = name
        self.terminator = terminator
        if action_to_output_map is None:
            self.action_to_output_map = {}
        else:
            self.action_to_output_map = action_to_output_map

    def _get_actions(self, output: str) -> None:
        if len(output) == 26:
            return latin
        elif len(output) == 36:
            return alphalatin
        else:
            raise AlphabetLengthException(output)

    def with_lower(self, output_list: str) -> None:
        outputs = output_list.split(',')

        actions = self._get_actions(outputs)

        for action, output in zip(actions.lower, outputs):
            self.action_to_output_map[action] = output

        return self


@dataclass(init=False, eq=True, repr=True, order=True)
class Action:
    id_: str = None
    next_: State = None

    def __init__(self, id_, next_=None):
        self.id_ = id_
        if next_ is not None:
            self.next_ = next_


@dataclass(init=False, eq=True, repr=True, order=True)
class Script:
    length: int = None
    lower: str = None
    upper: str = None

    def __init__(self, lower, upper=None, length=None) -> None:
        if len(lower) != len(upper):
            raise AlphabetLengthException(lower)  # TODO

        self.lower = lower
        self.length = len(lower)
        if upper is not None:
            self.upper = upper


latin = Script(
    lower='abcdefghijklmnopqrstuvwxyz',
    upper='ABCDEFGHIJKLMNOPQRSTUVWXYZ',
)


alphalatin = Script(
    lower=latin.lower + '1234567890',
    upper=latin.upper + '&@#$%^<>()',
)


actions_26_lower = latin.lower
actions_26_upper = latin.upper

actions_36_lower = alphalatin.lower
actions_36_upper = alphalatin.upper
