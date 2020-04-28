'''
@author Andrew J. Young
@description Unit tests for the file main.py
'''

# Imports from third party packages.
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import patch, mock_open, Mock, MagicMock, PropertyMock
from lxml.etree import Element
import os.path

# Package internal imports.
from symboard.keylayouts.keylayouts import Keylayout
from symboard.settings import VERSION
from symboard.file_writers import (
    FileWriter,
    KeylayoutFileWriter,
    KeylayoutXMLFileWriter,
    DEFAULT_OUTPUT_PATH,
)
from symboard.errors import (
    WriteException, KeylayoutNoneException, FileExistsException
)
from symboard.actions import State


file_writers_path = 'symboard.file_writers'


class TestFileWriter(TestCase):
    def setUp(self):
        self.file_writer = FileWriter()
        self.test_prefix = './hello/file'
        self.test_postfix = 'keylayout'

    def test_change_postfix_adds_postfix_when_no_match(self):
        test_path = self.test_prefix
        expected = self.test_prefix + '.' + self.test_postfix

        actual = self.file_writer._change_postfix(test_path, self.test_postfix)

        self.assertEqual(expected, actual)

    def test_change_postfix_corrects_incorrect_postfix(self):
        test_path = self.test_prefix + '.wrong_postfix'
        expected = self.test_prefix + '.' + self.test_postfix

        actual = self.file_writer._change_postfix(test_path, self.test_postfix)

        self.assertEqual(expected, actual)

    def test_change_postfix_does_nothing_when_correct_postfix(self):
        test_path = self.test_prefix + '.' + self.test_postfix
        expected = test_path

        actual = self.file_writer._change_postfix(test_path, self.test_postfix)

        self.assertEqual(expected, actual)

class TestKeylayoutFileWriter(TestFileWriter):
    def setUp(self):
        super().setUp()

        self.file_writer = KeylayoutFileWriter()
        self.test_output_path = 'actual.keylayout'
        self.mock = Mock()

    @patch(file_writers_path + '.exists')
    def test_write_opens_the_output_file_path(self, mock_exists):
        # Setup.
        mock_exists.return_value = False

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            with patch.object(self.file_writer.__class__, 'contents'):
                self.file_writer.write(self.mock, self.test_output_path)

            open_.assert_called_once_with(self.test_output_path, 'w+')

    @patch(file_writers_path + '.exists')
    def test_write_throws_exception_if_the_file_exists(self, mock_exists):
        mock_exists.return_value = True

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            with self.assertRaises(FileExistsException):
                self.file_writer.write(self.mock, self.test_output_path)

    @patch(file_writers_path + '.exists')
    def test_write_throws_exception_if_some_error_occurs(self, mock_exists):
        mock_exists.return_value = False

        with patch('builtins.open', 3) as open_:
            with self.assertRaises(WriteException):
                self.file_writer.write(self.mock, self.test_output_path)

    @patch(file_writers_path + '.exists')
    def test_write_allows_for_no_output_path(self, mock_exists):
        mock_exists.return_value = False

        with patch('builtins.open', mock_open(read_data='data')) as open_:
            with patch.object(self.file_writer.__class__, 'contents'):
                self.file_writer.write(self.mock)

            open_.assert_called_once_with(DEFAULT_OUTPUT_PATH, 'w+')


class TestKeylayoutXMLFileWriter(TestKeylayoutFileWriter):
    def setUp(self):
        super().setUp()

        self.expected_time = 'NOW'
        self.file_writer = KeylayoutXMLFileWriter()

        self.action_id = 'action'
        self.state_id = 'state'
        self.action_output = 'output'
        self.terminator = 'terminator'

    def test_contents_throws_exception_if_keylayout_is_none(self):
        with self.assertRaises(KeylayoutNoneException):
            self.file_writer.contents(None)

    def test_keyboard_has_correct_properties(self):
        expected_tag = 'keyboard'
        expected_attributes = {'test_attr': 'test_value'}

        mock_keylayout = self.mock
        mock_keylayout.keyboard_attributes = MagicMock(
            return_value=expected_attributes
        )

        element = self.file_writer._keyboard(mock_keylayout)

        self.assertEqual(expected_tag, element.tag)
        self.assertEqual(expected_attributes, element.attrib)

    def _comment(self, msg: str) -> str:
        """ Returns an XML comment (which contains <msg>) as a string.
        """
        return '<!-- {} -->'.format(msg)

    def test_comment_empty_string(self):
        msgs = [
            '',
            'test',
        ]
        for msg in msgs:
            expected = self._comment(msg)
            self.assertEqual(expected, self.file_writer._comment(msg))

    def _test_comment_with_strftime(self, function, comment):
        """ This class tests that <function> returns a comment with the string
        <comment>. It mocks out the time.strftime method, which allows it to
        test comments which include times in them.

        For symboard, it can be used to test both the «_created» and «_updated»
        functions.
        """
        time = self.mock
        time.strftime = MagicMock(return_value=self.expected_time)

        self.assertEqual(
            self._comment('Created by Symboard version {} at {}'.format(
                VERSION,
                self.expected_time,
            )),
            self.file_writer._created(time)
        )


    def test_created(self):
        self._test_comment_with_strftime(
            self.file_writer._created,
            f'Created by Symboard version {VERSION} at {self.expected_time}',
        )

    def test_updated(self):
        self._test_comment_with_strftime(
            self.file_writer._created,
            f'Last updated by Symboard version {VERSION} at' \
            f'{self.expected_time}',
        )

    def _assert_properties_of_XML_tag_returned_from(
        self, function, keylayout, expected_tag, expected_attributes, args=None
    ):
        if args is None:  # To avoid using mutable defaults.
            args = ()

        # We need to create this, as there's no way of finding a node's root,
        # only its children.
        # Without this object, we can't assert that the sub element is added as
        # its child.
        root = Element('root')

        child = function(keylayout, root, *args)

        self.assertEqual([child], list(root))
        self.assertEqual(expected_tag, child.tag)
        self.assertEqual(expected_attributes, child.attrib)

    def test_layouts_creates_a_well_formed_sub_element(self):
        """ Asserts that the sub_element created by «_layouts» meets the
        required specification.
        """
        mock_keylayout = self.mock
        mock_keylayout.layouts = MagicMock(return_value=[])

        self._assert_properties_of_XML_tag_returned_from(
            self.file_writer._layouts,
            keylayout=mock_keylayout,
            expected_tag='layouts',
            expected_attributes={},
        )

    def test_modifier_map_creates_a_well_formed_sub_element(self):
        """ Asserts that the sub_element created by «_modifier_map» meets the
        required specification.
        """

        # Warning: There are issues when using mocking with
        # lxml.etree.SubElement. This is in part because SubElement is
        # implemented using C. It is not possible to pass mock objects to
        # SubElement.
        EXPECTED_DEFAULT_INDEX = 3
        modifiers = 'Modifiers'

        keylayout = Keylayout(0, 0)
        keylayout.layouts = [{'modifiers': modifiers}]
        keylayout.default_index = str(EXPECTED_DEFAULT_INDEX)

        self._assert_properties_of_XML_tag_returned_from(
            self.file_writer._modifier_map,
            keylayout=keylayout,
            expected_tag='modifierMap',
            expected_attributes={
                'id': modifiers,
                'defaultIndex': str(EXPECTED_DEFAULT_INDEX),
            },
        )

    def test_key_map_set_creates_a_well_formed_sub_element(self):
        """ Asserts that the sub_element created by «_key_map_set» meets the
        required specification.
        """
        mock_keylayout = self.mock
        mock_keylayout.key_map = MagicMock(return_value=[])

        self._assert_properties_of_XML_tag_returned_from(
            self.file_writer._key_map_set,
            keylayout=mock_keylayout,
            expected_tag='keyMapSet',
            expected_attributes={'id': 'ANSI'},
        )

    def test_action_creates_well_formed_sub_element(self):
        ''' Warning: There are issues with using mocking and
        lxml.etree.SubElement. This is in part because SubElement is implemented
        using C. It is not possible to pass mock objects to SubElement. '''

        keylayout = Keylayout(0, 0)
        keylayout.states = [State(
            name=self.state_id,
            action_to_output_map={self.action_id: self.action_output},
        )]

        self._assert_properties_of_XML_tag_returned_from(
            self.file_writer._action,
            keylayout=keylayout,
            args=[self.action_id],
            expected_tag='action',
            expected_attributes={
                'id': self.action_id,
            },
        )

    def test_terminators_creates_well_formed_sub_element(self):
        ''' Warning: There are issues with using mocking and
        lxml.etree.SubElement. This is in part because SubElement is implemented
        using C. It is not possible to pass mock objects to SubElement. '''

        keylayout = Keylayout(0, 0)
        keylayout.states = [State(
            name=self.state_id,
            terminator=self.terminator,
        )]

        self._assert_properties_of_XML_tag_returned_from(
            self.file_writer._terminators,
            keylayout=keylayout,
            expected_tag = 'terminators',
            expected_attributes = {},
        )

    def test_layouts_creates_well_formed_sub_sub_elements(self):
        ## Begin setup #########################################################
        expected_tag = 'layout'
        expected_attributes = {'key': 'value'}

        root = Element('root')

        mock_keylayout = MagicMock(layouts=[expected_attributes])

        ########################################################### End setup ##
        ## Begin execution #####################################################
        modifier_map_elem = self.file_writer._layouts(mock_keylayout, root)

        grandchildren = root.findall('./layouts/layout')
        grandchild = grandchildren[0]

        ####################################################### End execution ##
        ## Begin assertion #####################################################
        self.assertEqual(1, len(grandchildren))
        self.assertEqual(expected_tag, grandchild.tag)
        self.assertEqual(expected_attributes, grandchild.attrib)
        ####################################################### End assertion ##

    def test_modifier_map_creates_well_formed_sub_sub_elements(self):
        ## Begin setup #########################################################
        expected_key_map_select_tag = 'keyMapSelect'
        expected_key_map_select_attributes = {'mapIndex': '0'}

        key_combos = ['test_keys_1', 'test_keys_2']
        expected_modifier_tag = 'modifier'

        root = Element('root')

        keylayout = Keylayout(0, 0)
        keylayout.key_map_select = {0: key_combos}
        keylayout.default_index = 6
        keylayout.layouts = [{'modifiers': expected_modifier_tag}]

        ########################################################### End setup ##
        ## Begin execution #####################################################
        modifier_map_elem = self.file_writer._modifier_map(keylayout, root)

        key_map_select_elems = root.findall('./modifierMap/keyMapSelect')
        modifier_elems = root.findall('./modifierMap/keyMapSelect/modifier')

        key_map_select_elem = key_map_select_elems[0]

        ####################################################### End execution ##
        ## Begin assertion #####################################################
        # Assertions for keyMapSelect
        self.assertEqual(1, len(key_map_select_elems))
        self.assertEqual(expected_key_map_select_tag, key_map_select_elem.tag)
        self.assertEqual(
            expected_key_map_select_attributes, key_map_select_elem.attrib
        )

        # Assertions for modifier
        self.assertEqual(2, len(modifier_elems))
        for i in range(len(modifier_elems)):
            modifier_elem = modifier_elems[i]
            expected_modifier_attributes = {'keys': key_combos[i]}

            self.assertEqual(expected_modifier_tag, modifier_elem.tag)
            self.assertEqual(
                expected_modifier_attributes, modifier_elem.attrib
            )
        ####################################################### End assertion ##

    def test_key_map_set_creates_well_formed_sub_sub_elements(self):
        ## Begin setup #########################################################
        expected_key_map_tag = 'keyMap'
        expected_key_map_attributes = {'index': '0'}

        expected_key_tag = 'key'
        expected_key_attributes = {'code': '3', 'output': 'v'}

        root = Element('root')

        mock_keylayout = MagicMock(key_map={
            0: {
                3: 'v',
            },
        })

        ########################################################### End setup ##
        ## Begin execution #####################################################
        key_map_elem = self.file_writer._key_map_set(mock_keylayout, root)

        key_map_elems = root.findall('./keyMapSet/keyMap')
        key_elems = root.findall('./keyMapSet/keyMap/key')

        key_map_elem = key_map_elems[0]
        key_elem = key_elems[0]

        ####################################################### End execution ##
        ## Begin assertion #####################################################
        # Assertions for keyMap
        self.assertEqual(1, len(key_map_elems))
        self.assertEqual(expected_key_map_tag, key_map_elem.tag)
        self.assertEqual(
            expected_key_map_attributes, key_map_elem.attrib
        )

        # Assertions for key
        self.assertEqual(1, len(key_elems))
        self.assertEqual(expected_key_tag, key_elem.tag)
        self.assertEqual(
            expected_key_attributes, key_elem.attrib
        )
        ####################################################### End assertion ##

    def test_action_creates_well_formed_sub_sub_element(self):
        ''' Warning: There are issues with using mocking and
        lxml.etree.SubElement. This is in part because SubElement is implemented
        using C. It is not possible to pass mock objects to SubElement. '''

        self.action_id = 'action'
        self.state_id = 'state'
        self.action_output = 'output'

        root = Element('root')

        keylayout = Keylayout(0, 0)
        keylayout.states = [State(
            name=self.state_id,
            action_to_output_map={self.action_id: self.action_output},
        )]

        expected_when_tag = 'when'
        expected_when_attributes = {
            'state': self.state_id,
            'output': self.action_output,
        }

        ########################################################### End setup ##
        ## Begin execution #####################################################

        child = self.file_writer._action(keylayout, root, self.action_id)

        when_elems = root.findall('./action/when')
        when_elem = when_elems[0]

        ####################################################### End execution ##
        ## Begin assertion #####################################################

        self.assertEqual(1, len(when_elems))
        self.assertEqual(expected_when_tag, when_elem.tag)
        self.assertEqual(
            expected_when_attributes, when_elem.attrib
        )

        ####################################################### End assertion ##

    def test_terminators_creates_well_formed_sub_sub_element(self):
        ''' Warning: There are issues with using mocking and
        lxml.etree.SubElement. This is in part because SubElement is implemented
        using C. It is not possible to pass mock objects to SubElement. '''

        self.state_id = 'state'
        self.terminator = 'terminator'

        root = Element('root')

        keylayout = Keylayout(0, 0)
        keylayout.states = [State(
            name=self.state_id,
            terminator=self.terminator,
        )]

        expected_when_tag = 'when'
        expected_when_attributes = {
            'state': self.state_id,
            'output': self.terminator,
        }

        ########################################################### End setup ##
        ## Begin execution #####################################################

        child = self.file_writer._terminators(keylayout, root)

        when_elems = root.findall('./terminators/when')
        when_elem = when_elems[0]

        ####################################################### End execution ##
        ## Begin assertion #####################################################

        self.assertEqual(1, len(when_elems))
        self.assertEqual(expected_when_tag, when_elem.tag)
        self.assertEqual(
            expected_when_attributes, when_elem.attrib
        )

        ####################################################### End assertion ##


if __name__ == '__main__':
    unittest_main()

