"""
.. module:: keylayouts
   :synopsis: A series of classes which describe classes about keyboards which
   are intended not be used on their own, but instead to be inherited from.

.. moduleauthor:: Andrew J. Young

"""


# Imports from third party packages.
from typing import Dict, List, Union
from dataclasses import dataclass, field

# Imports from the local package.
from symboard.actions import Action
from symboard.parsers import YamlFileParser


@dataclass
class Keylayout:
    """ A generic implementation of a keylayout, which should be inherited from
    by other keylayouts. It defines all the attributes and functions common to
    all keylayouts.

    Attributes:
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

    # Universal settings
    group: int = 126  # TODO: require?
    id_: int = -19341  # TODO: require?
    name: str = 'Untitled'
    maxout: int = 1  # TODO: fix this? Input validation?
    default_index: int = 0

    # These settings are configured by the child classes of «Keylayout».
    layouts: List[Dict[str, str]] = field(
        init=True, repr=False, compare=True, default_factory=list,
    )
    key_map_select: Dict[int, str] = field(
        init=True, repr=False, compare=True, default_factory=dict,
    )
    key_map: dict = field(
        init=True, repr=False, compare=True, default_factory=dict,
    )

    actions: set = field(
        init=False, repr=False, compare=False, default_factory=set,
    )
    used_states: list = field(
        init=False, repr=False, compare=False, default_factory=list,
    )
    states_list: list = field(
        init=False, repr=False, compare=False, default_factory=list,
    )

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

    def with_layouts(self, layouts):
        self.layouts = layouts
        return self

    def with_key_map(self, key_map):
        self.key_map = key_map
        return self

    def with_key_map_select(self, key_map_select):
        self.key_map_select = key_map_select
        return self

    def __str__(self):
        return 'Keylayout({}, (id: {}))'.format(self.name, self.id_)


class KeylayoutFactory:
    """ A class to create Keylayout object instances out of a variety of
    different formats.
    """
    def from_dict(contents: dict) -> Keylayout:
        """ Creates a keylayout from a dict. This dict can come from json or
        yaml files, for example. This dict should follow the specification for
        input dicts (for either yaml or json).

        Args:
            contents (dict): The dict to parse a keylayout from.
        """
        default_index = contents.get('default_index')
        group = contents.get('group')
        id_ = contents.get('id')
        maxout = contents.get('maxout')
        name = contents.get('name')

        key_map_select = contents['key_map_select']
        key_map = contents['key_map']
        # Note that this is in a list because of how the spec-writing
        # specification is defined.
        layouts = [contents['layouts']]

        return Keylayout(
            name = name,
            id_ = id_,
            maxout = maxout,
            group = group,
            default_index = default_index,
        ).with_layouts(
            layouts
        ).with_key_map(
            key_map
        ).with_key_map_select(
            key_map_select
        )

