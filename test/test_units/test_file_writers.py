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

        self.file_writer = KeylayoutXMLFileWriter()

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
        return '<!-- {} -->'.format(msg)

    def test_comment_empty_string(self):
        msg = ''
        expected = self._comment(msg)
        self.assertEqual(expected, self.file_writer._comment(msg))

    def test_comment_test_string(self):
        msg = 'test'
        expected = self._comment(msg)
        self.assertEqual(expected, self.file_writer._comment(msg))

    def test_created(self):
        expected_time = 'NOW'

        time = self.mock
        time.strftime = MagicMock(return_value=expected_time)

        self.assertEqual(
            self._comment('Created by Symboard version {} at {}'.format(
                VERSION,
                expected_time,
            )),
            self.file_writer._created(time)
        )

    def test_updated(self):
        expected_time = 'NOW'

        time = self.mock
        time.strftime = MagicMock(return_value=expected_time)

        self.assertEqual(
            self._comment('Last updated by Symboard version {} at {}'.format(
                VERSION,
                expected_time,
            )),
            self.file_writer._updated(time)
        )

    def test_layouts_creates_a_well_formed_sub_element(self):
        expected_tag = 'layouts'
        expected_attributes = {}

        # We need to create this, as there's no way of finding a node's parent,
        # only its children.
        # Without this object, we can't assert that the sub element is added as
        # its child.
        parent = Element('root')

        mock_keylayout = self.mock
        mock_keylayout.layouts = MagicMock(return_value=[])


        child = self.file_writer._layouts(mock_keylayout, parent)

        self.assertEqual([child], list(parent))
        self.assertEqual(expected_tag, child.tag)
        self.assertEqual(expected_attributes, child.attrib)

    def test_modifier_map_creates_a_well_formed_sub_element(self):
        EXPECTED_DEFAULT_INDEX = 3

        # We need to create this, as there's no way of finding a node's parent,
        # only its children.
        # Without this object, we can't assert that the sub element is added as
        # its child.
        parent = Element('root')

        mock_keylayout = self.mock
        mock_keylayout.key_map_select = MagicMock(return_value=[])
        mock_keylayout.default_index = EXPECTED_DEFAULT_INDEX

        expected_tag = 'modifierMap'
        expected_attributes = {
            'id': 'Modifiers',
            'defaultIndex': str(EXPECTED_DEFAULT_INDEX),
        }

        child = self.file_writer._modifier_map(mock_keylayout, parent)

        self.assertEqual([child], list(parent))
        self.assertEqual(expected_tag, child.tag)
        self.assertEqual(expected_attributes, child.attrib)

    def test_key_map_set_creates_a_well_formed_sub_element(self):
        expected_tag = 'keyMapSet'
        expected_attributes = {'id': 'ANSI'}

        # We need to create this, as there's no way of finding a node's parent,
        # only its children.
        # Without this object, we can't assert that the sub element is added as
        # its child.
        parent = Element('root')

        mock_keylayout = self.mock
        mock_keylayout.key_map = MagicMock(return_value=[])


        child = self.file_writer._key_map_set(mock_keylayout, parent)

        self.assertEqual([child], list(parent))
        self.assertEqual(expected_tag, child.tag)
        self.assertEqual(expected_attributes, child.attrib)

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

        mock_keylayout = MagicMock(key_map_select={0: key_combos})

        ########################################################### End setup ##
        ## Begin execution #####################################################
        modifier_map_elem = self.file_writer._modifier_map(mock_keylayout, root)

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


if __name__ == '__main__':
    unittest_main()

