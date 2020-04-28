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

        self.states_mocker = MagicMock(states = [State(
            name=self.state_id,
            action_to_output_map={self.action_id: self.action_output},
            terminator=self.terminator
        )])

    def test_contents_throws_exception_if_keylayout_is_none(self):
        with self.assertRaises(KeylayoutNoneException):
            self.file_writer.contents(None)

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

    def test_keyboard_has_correct_properties(self):
        expected_tag = 'keyboard'
        expected_attributes = {'test_attr': 'test_value'}

        mock_keylayout = self.mock
        mock_keylayout.keyboard_attributes = MagicMock(
            return_value=expected_attributes
        )

        elem = self.file_writer._keyboard(mock_keylayout)

        self.assertEqual(expected_tag, elem.tag)
        self.assertEqual(expected_attributes, elem.attrib)

    def _execute_function_on_elem(
        self, function, keylayout, args=None
    ):
        if args is None:  # To avoid using mutable defaults.
            args = ()

        # We need to create this, as there's no way of finding a node's root,
        # only its children.
        # Without this object, we can't assert that the sub elem is added as
        # its child.
        root = Element('root')

        return root, function(keylayout, root, *args)

    def _assert_properties_of_XML_tag_returned_from(
        self, function, expected_tag, expected_attributes, keylayout=None,
        args=None
    ):
        """ Assert that a function, when called on <keylayout> with an Element
        node and other arguments (provided by <args>) creates a sub-elem with
        the expected tag and attributes.

        <function>, given an Element node, should add a sub-elem to that
        node, and return the sub-elem.

        child_node = function(keylayout, Element('root'), *args)

        Args:
            function (Callable): The function under test.
            keylayout (Keylayout): The Keylayout, or mock object, being used to
            test <function>.
            expected_tag (str): The name that the sub-elem created by
            <function> is expected to have.
            expected_attributes (Dict[str, str]): A map of the expected
            attributes which the sub-elem created by <function> is expected
            to have.

        Raises:
            AssertionError: If the child is incorrectly created, or if either
            the expected tag or attributes are different to their actual values
            created by <function>.
        """
        root, child = self._execute_function_on_elem(
            function, keylayout, args
        )

        self.assertEqual([child], list(root))
        self.assertEqual(expected_tag, child.tag)
        self.assertEqual(expected_attributes, child.attrib)

    def test_layouts_creates_a_well_formed_sub_elem(self):
        """ Asserts that the sub_elem created by «_layouts» meets the
        required specification.
        """
        mock_keylayout = MagicMock(layouts=[])

        self._assert_properties_of_XML_tag_returned_from(
            self.file_writer._layouts,
            keylayout=mock_keylayout,
            expected_tag='layouts',
            expected_attributes={},
        )

    def test_modifier_map_creates_a_well_formed_sub_elem(self):
        """ Asserts that the sub_elem created by «_modifier_map» meets the
        required specification.
        """
        EXPECTED_DEFAULT_INDEX = 3
        modifiers = 'Modifiers'

        mock_keylayout = MagicMock(
            layouts=[{'modifiers': modifiers}],
            default_index=str(EXPECTED_DEFAULT_INDEX),
        )

        self._assert_properties_of_XML_tag_returned_from(
            self.file_writer._modifier_map,
            keylayout=mock_keylayout,
            expected_tag='modifierMap',
            expected_attributes={
                'id': modifiers,
                'defaultIndex': str(EXPECTED_DEFAULT_INDEX),
            },
        )

    def test_key_map_set_creates_a_well_formed_sub_elem(self):
        """ Asserts that the sub_elem created by «_key_map_set» meets the
        required specification.
        """
        mock_keylayout = MagicMock(key_map={})

        self._assert_properties_of_XML_tag_returned_from(
            self.file_writer._key_map_set,
            keylayout=mock_keylayout,
            expected_tag='keyMapSet',
            expected_attributes={'id': 'ANSI'},
        )

    def test_action_creates_well_formed_sub_elem(self):
        """ Asserts that the sub_elem created by «_action» meets the
        required specification.
        """
        self._assert_properties_of_XML_tag_returned_from(
            self.file_writer._action,
            keylayout=self.states_mocker,
            args=[self.action_id],
            expected_tag='action',
            expected_attributes={
                'id': self.action_id,
            },
        )

    def test_terminators_creates_well_formed_sub_elem(self):
        """ Asserts that the sub_elem created by «_terminators» meets the
        required specification.
        """
        mock_keylayout = MagicMock(states=[])

        self._assert_properties_of_XML_tag_returned_from(
            self.file_writer._terminators,
            keylayout=mock_keylayout,
            expected_tag='terminators',
            expected_attributes={},
        )

    def _assert_about_properties_of_sub_sub_elems(
        self, function, path_to_sub_elems, expected_tag, expected_attributes,
        args=None, expected_n_sub_elems=1, keylayout=None
    ):
        root, _ = self._execute_function_on_elem(function, keylayout, args)

        grandchildren = root.findall(path_to_sub_elems)
        n_sub_elems = len(grandchildren)

        self.assertEqual(expected_n_sub_elems, n_sub_elems)
        for i, grandchild in enumerate(grandchildren):
            self.assertEqual(expected_tag, grandchild.tag)
            if n_sub_elems == 1:
                self.assertEqual(expected_attributes, grandchild.attrib)
            else:
                self.assertEqual(expected_attributes[i], grandchild.attrib)


    def test_layouts_creates_well_formed_sub_sub_elems(self):
        expected_attributes = {'key': 'value'}

        mock_keylayout = MagicMock(layouts=[expected_attributes])

        self._assert_about_properties_of_sub_sub_elems(
            function=self.file_writer._layouts,
            keylayout=mock_keylayout,
            path_to_sub_elems='./layouts/layout',
            expected_tag='layout',
            expected_attributes=expected_attributes,
        )

        self._assert_about_properties_of_sub_sub_elems

    def test_modifier_map_creates_well_formed_sub_sub_elems(self):
        expected_modifier_tag = 'modifier'
        key_combos = ['test_keys_1', 'test_keys_2']

        mock_keylayout = MagicMock(
            key_map_select={0: key_combos},
            layouts=[{'modifiers': expected_modifier_tag}],
        )

        self._assert_about_properties_of_sub_sub_elems(
            self.file_writer._modifier_map,
            keylayout=mock_keylayout,
            path_to_sub_elems='./modifierMap/keyMapSelect',
            expected_tag='keyMapSelect',
            expected_attributes={'mapIndex': '0'},
        )

        self._assert_about_properties_of_sub_sub_elems(
            self.file_writer._modifier_map,
            keylayout=mock_keylayout,
            path_to_sub_elems='./modifierMap/keyMapSelect/modifier',
            expected_n_sub_elems = 2,
            expected_tag=expected_modifier_tag,
            expected_attributes=[
                {'keys': key_combos[i]} for i in range(len(key_combos))
            ],
        )

    def test_key_map_set_creates_well_formed_sub_sub_elems(self):
        mock_keylayout = MagicMock(key_map={
            0: {
                3: 'v',
            },
        })

        self._assert_about_properties_of_sub_sub_elems(
            self.file_writer._key_map_set,
            keylayout=mock_keylayout,
            path_to_sub_elems='./keyMapSet/keyMap',
            expected_tag='keyMap',
            expected_attributes={'index': '0'},
        )

        self._assert_about_properties_of_sub_sub_elems(
            self.file_writer._key_map_set,
            keylayout=mock_keylayout,
            path_to_sub_elems='.keyMapSet/keyMap/key',
            expected_tag='key',
            expected_attributes={'code': '3', 'output': 'v'},
        )

    def test_action_creates_well_formed_sub_sub_elem(self):
        self._assert_about_properties_of_sub_sub_elems(
            self.file_writer._action,
            keylayout=self.states_mocker,
            path_to_sub_elems='.action/when',
            args=[self.action_id],
            expected_tag='when',
            expected_attributes={
                'state': self.state_id,
                'output': self.action_output,
            },
        )

    def test_terminators_creates_well_formed_sub_sub_elem(self):
        self._assert_about_properties_of_sub_sub_elems(
            self.file_writer._terminators,
            keylayout=self.states_mocker,
            path_to_sub_elems='.terminators/when',
            expected_tag='when',
            expected_attributes={
                'state': self.state_id,
                'output': self.terminator,
            },
        )


if __name__ == '__main__':
    unittest_main()

