"""
.. module:: file_writers
   :synopsis: This file contains the definitions of classes which write to the
   local file system, and the methods they call in order to do so.

.. moduleauthor:: Andrew J. Young

"""

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
    WriteException, FileExistsException, KeylayoutNoneException
)
from symboard.keylayouts.keylayouts import Keylayout
from symboard.settings import VERSION, DEFAULT_OUTPUT_PATH


class FileWriter:
    """ The base class for functions which write to the local file system.

    Any classes which inherit from this class should have a custom
    implementation of «write».
    """
    def _change_postfix(self, path: str, extension: str) -> str:
        """ A function which returns a string of the given path which replaces
        the extension with the given extension.

        Args:
            path (str): The path which we want to check the extension of, and
                change if it mismatches with <extension>. This path does not
                need to include an extension.
            extension (str): The extension which we want the path to have.

        Returns:
            str: The full path, as provided, but with the extension specified by
                <extension>. If the provided path had an extension already,
                then this extenison is replaced. Otherwise, the provided
                extension is appended to the path.
        """

        # Assert postfix is non null and purely alphanumeric.
        prefix, old_extension = splitext(path)

        if old_extension != extension: # Incorrect or missing postfix.
            return prefix + '.' + extension
        else: # Correct postfix.
            return path

    def write(self, object_, output_path: str = DEFAULT_OUTPUT_PATH) -> None:
        """ A generic implementation of writing to file, which should be
        implemented by the children of this class.

        Args:
            object_ (object): The object we want to write data from.
            output_path (str): The path of the file we want to write to.
                Defaults to DEFAULT_OUTPUT_PATH.
        """
        pass


class KeylayoutFileWriter(FileWriter):
    def contents(self, keylayout: Keylayout) -> str:
        """ A generic implementation of getting the contents of a keylayout,
        which should be implemented by the children of this class.

        Args:
            keylayout (Keylayout): The keylayout we want to get the contents of.

        Returns:
            str: ''
        """
        return ''

    def write(
        self, keylayout: Keylayout, output_path: str = DEFAULT_OUTPUT_PATH
    ) -> None:
        """ Given an output file path, tries to create a file in that path using
        the contents of <keylayout>.

        Args:
            keylayout (Keylayout): The keylayout we want to write data from.
            output_path (str): The path of the file we want to write to.
                Defaults to DEFAULT_OUTPUT_PATH.

        Raises:
            FileExistsException: If <output_path> already exists.
            WriteException: If any error occurs while trying to create the
            contents of <keylayout>, or to write the contents to file.
        """

        # Ensure the file has the «.keylayout» postfix.
        output_path = self._change_postfix(output_path, 'keylayout')

        # Assert that the output_path is not already being used by any file
        # or directory.
        if exists(output_path):
            raise FileExistsException()

        try:
            contents = self.contents(keylayout)
            with open(output_path, 'w+') as file_:
                file_.write(contents)
        except:
            raise WriteException()


class KeylayoutXMLFileWriter(KeylayoutFileWriter):
    _DATE_FORMAT = "yyyy-MM-dd HH:mm:ss (UTC)"

    def contents(self, keylayout: Keylayout) -> str:
        """
        Args:
            keylayout (Keylayout): The keylayout we want to get the contents of.

        Returns:
            str: The (formatted) contents of <keylayout>, in XML version 1.1, in
            a format that can be read and installed by macOS.

        Raises:
            KeylayoutNoneException: If <keylayout> is None.
        """

        if keylayout is None:
            raise KeylayoutNoneException()

        now: datetime = datetime.now()

        prepend: str = '\n'.join([
            self._version(),
            '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">',
            self._created(now),
            self._updated(now),
        ])

        keyboard_elem: Element = self._keyboard(keylayout)

        self._layouts(keylayout, keyboard_elem)
        self._modifier_map(keylayout, keyboard_elem)
        self._key_map_set(keylayout, keyboard_elem)

        return '\n'.join([
            prepend,
            tostring(keyboard_elem, encoding='unicode', pretty_print=True),
        ])


    def _keyboard(self, keylayout: Keylayout) -> Element:
        """
        Args:
            keylayout (Keylayout): The keylayout we want to create a root
                element for.

        Returns:
            Element: An XML tag with the tag 'keyboard', and the attributes of
                <keylayout>. This element can have children added to it later.
        """
        return Element('keyboard', keylayout.keyboard_attributes())

    def _version(self) -> str:
        """
        Returns:
            str: A string specifying the version and encoding used by the class.
        """
        return '<?xml version="1.1" encoding="UTF-8"?>'

    def _comment(self, msg: str) -> str:
        """
        Returns:
            str: A string representing an XML comment containing the provided
            message.
        """
        return '<!-- {} -->'.format(msg)

    def _created(self, time: datetime) -> str:
        """
        Returns:
            str: A string representing an XML comment containing the version of
            symboard which is being used, and the date and time at which the
            comment was created.
        """
        return self._comment('Created by Symboard version {} at {}'.format(
            VERSION, time.strftime(self._DATE_FORMAT)
        ))

    def _updated(self, time: datetime) -> str:
        """
        Returns:
            str: A string representing an XML comment containing the version of
            symboard which is being used, and the date and time at which the
            comment was created (as this is equal to its last update time).
        """
        return self._comment('Last updated by Symboard version {} at {}'.format(
            VERSION, time.strftime(self._DATE_FORMAT)
        ))

    def _layouts(self, keylayout: Keylayout, keyboard: Element) -> Element:
        """
        Args:
            keylayout (Keylayout): The keylayout to create a «layouts» element
                from.
            keyboard (Element): The XML Element which is to be the parent of the
            newly created «layouts» element.

        Returns:
            Element: An element which has been added as a child to <keyboard>,
            containing the tag «layouts». It has children with the tag «layout»,
            each containing attributes as specified by the attributes in
            <keylayout.layouts>.
        """
        layouts_elem: Element = sub_element(keyboard, 'layouts')

        # Create children to the layouts_elem
        for layout_attributes in keylayout.layouts:
            sub_element(layouts_elem, 'layout', layout_attributes)

        return layouts_elem

    def _modifier_map(self, keylayout: Keylayout, keyboard: Element) -> Element:
        """
        Args:
            keylayout (Keylayout): The keylayout to create a «layouts» element
                from.
            keyboard (Element): The XML Element which is to be the parent of the
            newly created «layouts» element.

        Returns:
            Element: An element which has been added as a child to <keyboard>,
            containing the tag «modiferMap». It has children with the tag
            «keyMapSelect», which themselves have children with the tag
            «modifier». Each of these elements contains attributes as specified
            by the dictionary in <keylayout.key_map_select>.
        """
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
            key_map_select_elem: Element = sub_element(
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

    def _key_map_set(self, keylayout: Keylayout, keyboard: Element) -> Element:
        """
        Args:
            keylayout (Keylayout): The keylayout to create a «layouts» element
                from.
            keyboard (Element): The XML Element which is to be the parent of the
            newly created «layouts» element.

        Returns:
            Element: An element which has been added as a child to <keyboard>,
            containing the tag «keyMapSet». It has children with the tag
            «keyMap», which themselves have children with the tag «keys». Each
            of these elements contains attributes as specified by the dictionary
            in <keylayout.key_map>.
        """
        key_map_set_elem: Element = sub_element(
            keyboard, 'keyMapSet', {'id': 'ANSI'}
        )

        # Create children to the key_map_set_elem
        for i, key_map in keylayout.key_map.items():
            key_map_elem: Element = sub_element(
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

