'''@author: Andrew J. Young
@description: A file writer, which given input will output this as formatted
data to a specified output file.
'''

# Imports from third party packages.
from os.path import exists, splitext
from re import search
from lxml.etree import (
    Element,
    SubElement as sub_element,
    tostring,
)
from datetime import datetime

# Package internal imports.
from symboard.errors import (
    WriteException, FileExistsException, ContentsNoneException
)
from symboard.keylayouts.keylayouts import Keylayout
from symboard.settings import VERSION


DEFAULT_OUTPUT_PATH = './a.keylayout'


class FileWriter:
    def change_postfix(self, path: str, new_postfix: str) -> str:
        # Assert postfix is non null and purely alphanumeric.
        prefix, old_postfix = splitext(path)

        if old_postfix != new_postfix: # Incorrect or missing postfix.
            return prefix + '.' + new_postfix
        else: # Correct postfix.
            return path

    def write(self, object_, output_path: str = DEFAULT_OUTPUT_PATH):
        pass


class KeylayoutFileWriter(FileWriter):
    def contents(self, keylayout: Keylayout) -> str:
        # Defined by the children of this class.
        return ''

    def write(
        self, keylayout: Keylayout, output_path: str = DEFAULT_OUTPUT_PATH
    ) -> None:
        ''' Given an output file path, creates a file in that file path.
        Assumes the file is not already present. Throws an error if this
        is not true.
        '''

        # Ensure the file has the «.keylayout» postfix.
        output_path = self.change_postfix(output_path, 'keylayout')

        # Assert that the output_path is not already being used by any file
        # or directory.
        if exists(output_path):
            raise FileExistsException()

        try:
            with open(output_path, 'w+') as file_:
                file_.write(self.contents(keylayout))
        except:
            raise WriteException()


class KeylayoutXMLFileWriter(KeylayoutFileWriter):
    def contents(self, keylayout: Keylayout) -> str:
        if keylayout is None:
            raise ContentsNoneException()

        prepend = '\n'.join([
            self.version(),
            '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">',
            self.created(),
            self.updated(),
        ])

        keyboard_elem = self.keyboard(keylayout)

        self.layouts(keylayout, keyboard_elem)
        self.modifier_map(keylayout, keyboard_elem)
        self.key_map_set(keylayout, keyboard_elem)

        return '\n'.join([
            prepend,
            tostring(keyboard_elem, encoding='unicode', pretty_print=True),
        ])


    def keyboard(self, keylayout: Keylayout) -> Element:
        return Element('keyboard', keylayout.keyboard_attributes())

    def version(self) -> str:
        return '<?xml version="1.1" encoding="UTF-8"?>'

    def comment(self, msg: str) -> str:
        return '<!-- {} -->'.format(msg)

    def created(self) -> str:
        return self.comment('Created by Symboard version {} at {}'.format(
            VERSION, datetime.utcnow() # TODO: ISO
        ))

    def updated(self) -> str:
        return self.comment('Last updated by Symboard version {} at {}'.format(
            VERSION, datetime.utcnow() # TODO: ISO
        ))

    def layouts(self, keylayout: Keylayout, keyboard: Element) -> Element:
        layouts_elem = sub_element(keyboard, 'layouts')

        # Create children to the layouts_elem
        for layout_attributes in keylayout.layouts:
            sub_element(layouts_elem, 'layout', layout_attributes)

        return layouts_elem

    def modifier_map(self, keylayout: Keylayout, keyboard: Element) -> Element:
        modifier_map_elem = sub_element(
            keyboard,
            'modifierMap',
            {
                'id': 'Modifiers',
                'defaultIndex': str(keylayout.default_index),
            },
        )

        # Create children to the modifier_map_elem
        for key, value in keylayout.key_map_select.items():
            key_map_select_elem = sub_element(
                modifier_map_elem,
                'keyMapSelect',
                {'mapIndex': str(key)},
            )
            sub_element(
                key_map_select_elem,
                'modifier',
                {'keys': str(value)},
            )

        return modifier_map_elem

    def key_map_set(self, keylayout: Keylayout, keyboard: Element) -> Element:
        key_map_set_elem = sub_element(keyboard, 'keyMapSet', {'id': 'ANSI'})

        # Create children to the key_map_set_elem
        for i, key_map in keylayout.key_map.items():
            key_map_elem = sub_element(
                key_map_set_elem,
                'keyMap',
                {'index': str(i)},
            )
            for code, output in key_map.items():
                sub_element(
                    key_map_elem,
                    'key',
                    {'code': str(code), 'output': str(output)}
                )

        return key_map_set_elem

