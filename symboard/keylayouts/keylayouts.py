'''
@author: Andrew J. Young
@description: A series of classes which describe classes about keyboards which
are intended not be used on their own, but instead to be inherited from.
'''

# Imports from third party packages.
from typing import Dict, List, Union


class Keylayout:
    # Universal defaults
    DEFAULT_NAME: str = 'Untitled'

    # Universal settings
    group: int = 126
    id_: int = -19341
    name: str = DEFAULT_NAME
    maxout: int = 1
    default_index: int = 0

    # These settings are configured by the child classes of «Keylayout».
    layouts: List[Union[str, str]] = []
    key_map_select: Dict[int, str] = {}
    key_map: Dict[int, Dict[str, str]] = {}

    def keyboard_attributes(self):
        return {
            'group': keylayout.group,
            'id': keylayout.id_,
            'name': keylayout.name,
            'maxout': keylayout.maxout,
        }

    def __str__(self):
        return 'Keylayout({}, (id: {}))'.format(self.name, self.id_)

    def __init__(
        self,
        group: int,
        id_: int,
        name: str,
        maxout: int,
        default_index: int = 0
    ):
        self.group = group
        self.id_ = id_
        self.name = name
        self.maxout = maxout
        self.default_index = default_index

