#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: file_writers
   :synopsis: This file contains the definitions of classes which write to the
   local file system, and the methods they call in order to do so.

.. moduleauthor:: Andrew J. Young

"""

# Imports from third party packages.
from os.path import exists, splitext
from re import search, sub
from lxml.etree import (
    Element,
    SubElement as sub_element,
    tostring,
)
from datetime import datetime
import logging

# Package internal imports.
from symboard.errors import (
    WriteException, FileExistsException, KeylayoutNoneException
)
from symboard.keylayouts.keylayouts import Keylayout, Action
from settings import VERSION, DEFAULT_OUTPUT_PATH


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

        if old_extension != extension:  # Incorrect or missing postfix.
            return prefix + '.' + extension
        else:  # Correct postfix.
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
        self, keylayout: Keylayout,
        output_path: str = DEFAULT_OUTPUT_PATH,
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
            raise FileExistsException(output_path)

        try:
            contents = self.contents(keylayout)

            logging.info(f'Writing disk contents at {output_path}.')

            with open(output_path, 'w+') as file_:
                file_.write(contents)
        except:
            raise WriteException(output_path)


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

        logging.info(f'Getting contents for keylayout {repr(keylayout)}.')

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
        if len(keylayout.actions) > 0:
            self._actions(keylayout, keyboard_elem)
        if len(keylayout.used_states) > 0:
            self._terminators(keylayout, keyboard_elem)

        ''' Right. So the authors of the «XML» package assumed, wrongly, that we
        would always want to escape «&» by default. In fact, we pretty much
        exclusively want &# to *not* be escaped (unless it's on its own).

        I've looked around, and there are no low-effort solutions to this
        problem that aren't total hacks.

        So let's just regex replace all unicode strings.
        '''
        stupidly_escaped_contents = '\n'.join([
            prepend,
            tostring(keyboard_elem, encoding='unicode', pretty_print=True),
        ])

        return sub(r'&amp;#x', '&#x', stupidly_escaped_contents)

    def _get_tag(self, object_: object):
        """ Returns "output" if <object_ > is a string, and "action" if it is an
        Action. Raises an exception otherwise.

        This corresponds to the behavior of the keylayout XML files. If a key
        being pressed is meant to produce output, then the tag must be
        «output», otherwise it must be «action» if an action is triggered by it
        (such as entering a state).

        Args:
            object_ (object): The object to get the tag for.

        Raises:
            TagNotFoundException: If the object_ is neither a string nor an
            Action, and hence a tag is unable to be generated.
        """
        if isinstance(object_, str):
            return 'output'
        elif isinstance(object_, Action):
            return 'action'
        else:
            raise TagNotFoundException(object_)

    def _get_output(self, object_: object):
        """ Returns the output for when a key is pressed, based off «object_»
        from a key map. If the output is a normal key, the output will be a
        string (and hence type regular text). If the output is an action, the
        output will be triggering that action.

        Args:
            object_ (object): The object (from a key map) to get the output for.

        Raises:
            CouldNotGetOutputException: If the output from <object_> could not
            be resolved (IE <object_> is not a string or an Action).
        """
        if isinstance(object_, str):
            return object_
        elif isinstance(object_, Action):
            return object_.id_
        else:
            raise CouldNotGetOutputException(object_)

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
        logging.info(f'Creating a layouts element and its subchildren.')

        layouts_elem: Element = sub_element(keyboard, 'layouts')

        # Create children to the layouts_elem
        for layout_attributes in keylayout.layouts:
            sub_element(layouts_elem, 'layout', layout_attributes)

        return layouts_elem

    def _modifier_map(self, keylayout: Keylayout, keyboard: Element) -> Element:
        """
        Args:
            keylayout (Keylayout): The keylayout to create a «modifierMap» element
                from.
            keyboard (Element): The XML Element which is to be the parent of the
            newly created «modifierMap» element.

        Returns:
            Element: An element which has been added as a child to <keyboard>,
            containing the tag «modiferMap». It has children with the tag
            «keyMapSelect», which themselves have children with the tag
            «modifier». Each of these elements contains attributes as specified
            by the dictionary in <keylayout.key_map_select>.
        """
        logging.info(f'Creating a modifierMap element and its subchildren.')

        modifier_map_elem = sub_element(
            keyboard,
            'modifierMap',
            {
                'id': keylayout.layouts[0]['modifiers'],
                'defaultIndex': str(keylayout.default_index),
            },
        )

        # Create children to the modifier_map_elem
        for key, key_strokes in keylayout.key_map_select.items():
            key_map_select_elem: Element = sub_element(
                modifier_map_elem,
                'keyMapSelect',
                {'mapIndex': str(key)},
            )
            for key_stroke in key_strokes:
                sub_element(
                    key_map_select_elem,
                    'modifier',
                    {'keys': str(key_stroke)},
                )

        return modifier_map_elem

    def _key_map_set(self, keylayout: Keylayout, keyboard: Element) -> Element:
        """
        Args:
            keylayout (Keylayout): The keylayout to create a «keyMap» element
                from.
            keyboard (Element): The XML Element which is to be the parent of the
                newly created «keyMap» element.

        Returns:
            Element: An element which has been added as a child to <keyboard>,
            containing the tag «keyMapSet». It has children with the tag
            «keyMap», which themselves have children with the tag «keys». Each
            of these elements contains attributes as specified by the dictionary
            in <keylayout.key_map>.
        """
        logging.info(f'Creating a keyMap element and its subchildren.')

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
                    {
                        'code': str(code),
                        self._get_tag(output): self._get_output(output)
                    },
                )

        return key_map_set_elem

    def _actions(self, keylayout: Keylayout, keyboard: Element) -> Element:
        logging.info(f'Creating an actions element and its subchildren.')

        actions_elem: Element = sub_element(
            keyboard, 'actions'
        )

        for action in sorted(keylayout.actions):
            self._action(keylayout, actions_elem, action)

        return actions_elem

    def _when_elem(
        self, elem: Element, state: str, output_type: str, output: object
    ) -> Element:
        return sub_element(
            elem,
            'when',
            {
                'state': state,
                output_type: output,
            }
        )

    def _action(
        self, keylayout: Keylayout, keyboard: Element, action: Action
    ) -> Element:
        """
        Args:
            keylayout (Keylayout): The keylayout to create an «action» element
                from.
            keyboard (Element): The XML Element which is to be the parent of the
                newly craeted «action» element.
            action_id (str): The unique id (name) to give to the action.

        Returns:
            Element: An element which has been added as a child to <keyboard>,
            containing the tag «action», and an id for that action. The action
            tag has children with the tag «when». Each of these tags specifies
            the output when the action accurs in a particular state.
        """
        if keylayout.used_states is None:
            return

        action_id = action.id_
        next_state = action.next_

        action_elem: Element = sub_element(
            keyboard, 'action', {'id': action_id}
        )

        if next_state is not None:
            # Add a dead key (the "next" output will be the state the user
            # enters next.
            next_state_name = next_state.name
            self._when_elem(action_elem, 'none', 'next', next_state_name)
        else:
            output = action_id
            self._when_elem(action_elem, 'none', 'output', output)

        for state in keylayout.used_states:
            # Add an output for the "none" state, including possible dead keys.
            if action_id in state.action_to_output_map.keys():
                self._when_elem(
                    action_elem, state.name, 'output',
                    state.action_to_output_map[action_id],
                )

        return action_elem

    def _terminators(self, keylayout: Keylayout, keyboard: Element) -> Element:
        """
        Args:
            keylayout (Keylayout): The keylayout to create a «terminators» element
                from.
            keyboard (Element): The XML Element which is to be the parent of the
                newly craeted «terminators» element.

        Returns:
            Element: An element which has been added as a child to <keyboard>,
            containing the tag «terminators». The terminators tag has children
            with the tag «when». These tags specify the terminators for each
            state of <keylayout>.
        """
        logging.info(f'Creating a terminators element and its subchildren.')

        terminators_elem: Element = sub_element(
            keyboard, 'terminators'
        )

        for state in keylayout.used_states:
            self._when_elem(
                terminators_elem, state.name, 'output', state.terminator
            )

        return terminators_elem
