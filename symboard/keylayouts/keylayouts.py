"""
.. module:: keylayouts
   :synopsis: A series of classes which describe classes about keyboards which
   are intended not be used on their own, but instead to be inherited from.

.. moduleauthor:: Andrew J. Young

"""


# Imports from third party packages.
from typing import Dict, List, Union
from dataclasses import dataclass

# Imports from the local package.
from symboard.actions import Action


class Keylayout:
    """ A generic implementation of a keylayout, which should be inherited from
    by other keylayouts. It defines all the attributes and functions common to
    all keylayouts.

    Attributes:
        _DEFAULT_NAME (str): The default name for a keyboard, if no name is
            provided.

        group (int): The group number for the keyboard.
        id_ (int): The unique ID number for the keyboard, which should be some
            random number in the range [..].
        name (str): The name of the keyboard. Defaults to <_DEFAULT_NAME>
        maxout (int): The max number of unicode characters which can be output
            at a time. Defaults to 1.
        default_index (int): The default index for the keyboard. The default
            index is used when some key combination is being pressed that meets
            none of the states defined in key_map_select.

        layouts (list): A list containing the attributes of each layout of the
            keyboard. The attributes provided are:
                - first (index)
                - last  (index)
                - mapSet (the key map set being used. For us, this is always the
                  class of the keyboard.
                - modifiers (The modifier set being used. For us, this is always
                  set to 'Modifiers'.

            You generally don't want or need to edit these attributes. More
            comprehensive information about what they do can be found online.
        key_map_select (Dict[int, str]): A list containing the states of the
            keyboard, and the string of the keys which will cause that state to
            be entered if they are pressed.
        key_map (Dict[int, Dict[int, str]]): A dictionary containing the
            mappings of all inputs and outputs of the keyboard, for all states.
    """

    # Universal defaults
    _DEFAULT_NAME: str = 'Untitled'

    # Universal settings
    group: int = 126
    id_: int = -19341
    name: str = _DEFAULT_NAME
    maxout: int = 1
    default_index: int = 0

    # These settings are configured by the child classes of «Keylayout».
    layouts: List[Dict[str, str]] = []
    key_map_select: Dict[int, str] = {}
    key_map: dict = {}

    actions: set = set()
    used_states: list = list()
    states_list: list = list()

    def keyboard_attributes(self):
        """
        Returns:
            (Dict[int, str]): A dictionary containing the following attributes
                of the current keyboard:
                    - group
                    - id
                    - name
                    - maxout
        """
        return {
            'group':  str(self.group),
            'id':     str(self.id_),
            'name':   str(self.name),
            'maxout': str(self.maxout),
        }

    def set_actions_from_key_map(self):
        self.actions = [
            output
            for index in self.key_map.values()
            for key, output in index.items()
            if isinstance(output, Action)
        ]

    def create_used_states(self, states) -> bool:
        self.used_states = [
            states[state_name] for state_name in self.states_list
        ]

    def __str__(self):
        return 'Keylayout({}, (id: {}))'.format(self.name, self.id_)

    def __init__(
        self,
        group: int,
        id_: int,
        maxout: int = 1,
        name: str = _DEFAULT_NAME,
        default_index: int = 0
    ):
        self.group = group
        self.id_ = id_
        self.maxout = maxout
        self.name = name
        self.default_index = default_index
        self.set_actions_from_key_map()

