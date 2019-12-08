"""
.. module:: keylayouts
   :synopsis: A series of classes which describe classes about keyboards which
   are intended not be used on their own, but instead to be inherited from.

.. moduleauthor:: Andrew J. Young

"""


# Imports from third party packages.
from typing import Dict, List, Union


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
        maxout (int): Todo
        default_index (int): The default index for the keyboard.

        layouts (list): A list containing the layouts of the keylayout.
        key_map_select (Dict[int, str]): A list containing the states of the
            keyboard, and the string of the keys which will cause that state to
            be entered if they are pressed.
        key_map (Dict[int, Dict[int, str]]): A dictionary containing the
            mappings of all inputs and outputs of the keyboard, for all states.
    """
    # TODO More info on attributes.

    # Universal defaults
    _DEFAULT_NAME: str = 'Untitled'

    # Universal settings
    group: int = 126
    id_: int = -19341
    name: str = _DEFAULT_NAME
    maxout: int = 1
    default_index: int = 0

    # These settings are configured by the child classes of «Keylayout».
    layouts: list = [] # TODO: fix type signature.
    key_map_select: Dict[int, str] = {}
    key_map: Dict[int, Dict[int, str]] = {}

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

    def __str__(self):
        return 'Keylayout({}, (id: {}))'.format(self.name, self.id_)

    def __init__(
        self,
        group: int,
        id_: int,
        maxout: int,
        name: str = _DEFAULT_NAME,
        default_index: int = 0
    ):
        self.group = group
        self.id_ = id_
        self.maxout = maxout
        self.name = name
        self.default_index = default_index

