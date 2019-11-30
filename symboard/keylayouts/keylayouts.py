'''
@author: Andrew J. Young
@description: A series of classes which describe classes about keyboards which
are intended not be used on their own, but instead to be inherited from.
'''

# Imports from third party packages.
from typing import Dict
from numbers import Number
from datetime import datetime
from xml.etree.ElementTree import SubElement, Comment

VERSION = '0.0'

class KeylayoutWriter:
    def created(self) -> Comment:
        return Comment('Created by Symboard version {} at {}'.format(
            VERSION, datetime.utcnow()
        ))

    def updated(self) -> Comment:
        return Comment('Last updated by Symboard version {} at {}'.fromat(
            VERSION, datetime.utcnow()
        ))

    @staticmethod
    def keyboard_attributes(keylayout: Keylayout) -> Dict[str, str]:_
        return {
            'group' = keylayout.group,
            'id' = keylayout.id_,
            'name' = keylayout.name,
            'maxout' = keylayout.maxout,
        }

    def layouts(self, keylayout: Keylayout, keyboard: Element) -> SubElement:
        layouts = SubElement(keyboard, 'layouts')
        [SubElement(layouts, layout.attrib) for layout in keylayout.layouts]
        return layouts

    def modifier_map(self, keyboard: Element) -> SubElement:
        modifier_map = SubElement(
            keyboard,
            'modifierMap',
            {
                'id': 'Modifiers',
                'defaultIndex': keylayout.modifier_map.default_index,
            }
        )

        for key_map_select, i in enumerate(keylayout.modifier_map):
            key_map_select_elem = SubElement(
                modifier_map,
                'keyMapSelect',
                {'mapIndex': index},
            )
            SubElement(
                key_map_select_elem,
                'modifier',
                {'keys': keyboard.keys_to_string(key_map_select.keys)},
            )

        return modifier_map

    def key_map_set(
            self, keylayout: Keylayout, keyboard: Element
    ) -> SubElement:

        key_map_set_elem = SubElement(keyboard, 'keyMapSet', {'id': 'ANSI'})
        for key_map, i in enumerate(keyboard.key_map_set):
            key_map_elem = SubElement(key_map_set_elem, 'key_map', {'index': i})
            for key, value in keyboard.key_dict.items():
                SubElement(key_map_elem, 'key', {'code': key, 'output': value})

        return key_map_set

    def keyboard(self, keylayout) -> Element:
        keyboard = Element('keyboard', keyboard_attributes(keylayout))

        # Children of «keyboard»
        layouts()
        modifier_map()
        key_map_set()

        return keyboard


class Keylayout:
    # Universal settings
    group: int = 126
    id_: int = -19341
    name: str = 'Untitled'
    maxout: int = 1

    # These settings are configured by the child classes of «Keylayout».
    layouts: set = {}
    key_map_select: Dict[int, str] = {}
    key_map: Dict[int, Dict[str, str] = {}

    def __str__(self):
        return 'Keylayout({}, (id: {}))'.format(self.name, self.id_)

