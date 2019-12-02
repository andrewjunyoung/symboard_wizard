'''
@author: Andrew J. Young
@description: A file writer, which given input will output this as formatted
data to a specified output file.
'''

# Third party package imports
from os.path import exists, splitext
from re import search
from xml.etree.ElementTree import (
    Comment as comment,
    Element as Element,
    SubElement as SubElement,
    tostring,
)
from datetime import datetime

# Package internal imports
from symboard.errors import WriteException, FileExistsException
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
        keyboard_elem = self.keyboard(keylayout)

        self.layouts(keylayout, keyboard_elem)
        self.modifier_map(keylayout, keyboard_elem)
        self.key_map_set(keylayout, keyboard_elem)

        # TODO: Write return statement.
        # TODO: ¿How to incorporate created(); updated()?
        return '\n'.join([
            tostring(keyboard_elem, encoding="UTF-8")
        ])

    def keyboard(self, keylayout: Keylayout) -> Element:
        return Element('keyboard', keylayout.keyboard_attributes())

    def created(self) -> None:
        comment('Created by Symboard version {} at {}'.format(
            VERSION, datetime.utcnow()
        ))

    def updated(self) -> None:
        comment('Last updated by Symboard version {} at {}'.format(
            VERSION, datetime.utcnow()
        ))

    def layouts(self, keylayout: Keylayout, keyboard: Element) -> None:
        layouts_elem = SubElement(keyboard, 'layouts')
        for layout in keylayout.layouts:
            SubElement(layouts_elem, layout)

    def modifier_map(self, keylayout: Keylayout, keyboard: Element) -> None:
        modifier_map_elem = SubElement(
            keyboard,
            'modifierMap',
            {
                'id': 'Modifiers',
                'defaultIndex': str(keylayout.default_index)
            },
        )

        for key_map_select, i in enumerate(keylayout.key_map_select):
            key_map_select_elem = SubElement(
                modifier_map_elem,
                'keyMapSelect',
                {'mapIndex': str(i)},
            )
            SubElement(
                key_map_select_elem,
                'modifier',
                {'keys': keylayout.key_map_select[i]}
            )

    def key_map_set(self, keylayout: Keylayout, keyboard: Element) -> None:

        key_map_set_elem = SubElement(keyboard, 'keyMapSet', {'id': 'ANSI'})
        for key_map, i in enumerate(keylayout.key_map_select):
            key_map_elem = SubElement(
                key_map_set_elem,
                'key_map',
                {'index': str(i)},
            )
            for key, value in keylayout.key_map[i].items():
                SubElement(key_map_elem, 'key', {'code': key, 'output': value})

