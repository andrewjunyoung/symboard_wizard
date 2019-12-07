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
    layouts: list = [] # TODO: fix type signature.
    key_map_select: Dict[int, str] = {}
    key_map: Dict[int, Dict[int, str]] = {}

    def keyboard_attributes(self):
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
        name: str = DEFAULT_NAME,
        default_index: int = 0
    ):
        self.group = group
        self.id_ = id_
        self.maxout = maxout
        self.name = name
        self.default_index = default_index

