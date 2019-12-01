'''
@author: Andrew J. Young
@description: A file writer, which given input will output this as formatted
data to a specified output file.
'''

# Package internal imports
from symboard.errors import WriteException

# Third party package imports
from os.path import exists


DEFAULT_OUTPUT_PATH = './a.keylayout'


class FileWriter:
    def change_suffix(self, path: str, suffix: str) -> str:
        # Assert suffix is non null and purely alphanumeric.
        assert match(r'^[a-zA-Z0-9]+$', suffix) # TODO: Check if can be simplified.
        result = match(r'^.*(\.(*))$', string)

        if no_suffix:
            return path + suffix
        elif right_suffix
            return path
        else: # There is a suffix, but it's the wrong one.
            return path + '.' + suffix

        return path

    def write(self):
        pass


class KeylayoutFileWriter(FileWriter):
    def contents(self, keylayout: Keylayout) -> str:
        # Defined by the children of this class.
        return ''

    def write(
        self, keylayout, Keylayout, output_file_path: str = DEFAULT_OUTPUT_PATH
    ) -> None:
        ''' Given an output file path, creates a file in that file path.
        Assumes the file is not already present. Throws an error if this
        is not true.
        '''

        # Ensure the file has the «.keylayout» suffix.
        output_path: str = change_suffix(output_path, 'keylayout')

        # Assert that the output_file_path is not already being used by any file
        # or directory.
        if exists(output_file_path):
            WriteException()

        try:
            with open() as file_:
                file_.write(self.contents())
        except:
            WriteException()


class KeylayoutXMLFileWriter(KeylayoutFileWriter):
    def contents(self, keylayout: Keylayout) -> List[str]:
        keyboard = self.keyboard(keylayout)

        self.layouts(keylayout, keyboard)
        self.modifier_map(keylayout, keyboard)
        self.key_map_set(keylayout, keyboard)

        return '\n'.join([
            self.created(),
            self.updated(),
            tostring(keyboard, encoding="UTF-8")
        ])

    def keyboard(self, keylayout: Keylayout) -> Element:
        return Element('keyboard', keylayout.keyboard_attributes())

    def created(self) -> Comment:
        return Comment('Created by Symboard version {} at {}'.format(
            VERSION, datetime.utcnow()
    from numbers import Number
        ))

    def updated(self) -> Comment:
        return Comment('Last updated by Symboard version {} at {}'.format(
            VERSION, datetime.utcnow()
        ))

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

