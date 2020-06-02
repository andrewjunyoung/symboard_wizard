# Imports from third party packages.
from unittest import TestCase
from unittest import main as unittest_main

# Imports from the local package.
from symboard.keylayouts import KeylayoutFactory
from symboard.utils.collections import convert_items_to_str


keylayout_factory = KeylayoutFactory()


class TestKeylayout(TestCase):
    __test__ = False

    def _setUp(self, base_layout):
        self.GROUP = 1
        self.ID = 2
        self.NAME = '3'
        self.MAXOUT = 4
        self.DEFAULT_INDEX = 5

        self.keylayout_factory = keylayout_factory
        self.spec = {
            'base_layout': base_layout,
            'group': self.GROUP,
            'id': self.ID,
            'name': self.NAME,
            'maxout': self.MAXOUT,
            'default_index': self.DEFAULT_INDEX,
        }
        self.keylayout = self.keylayout_factory.from_spec(self.spec)

    def test_keylayout_init_with_all_properties_provided(self):
        keylayout = self.keylayout

        self.assertEqual(keylayout.group, self.GROUP)
        self.assertEqual(keylayout.id_, self.ID)
        self.assertEqual(keylayout.name, self.NAME)
        self.assertEqual(keylayout.maxout, self.MAXOUT)
        self.assertEqual(keylayout.default_index, self.DEFAULT_INDEX)

    def test_keylayout_init_without_default_index(self):
        spec = self.spec.copy()
        del spec['default_index']
        keylayout = self.keylayout_factory.from_spec(spec)

        self.assertEqual(keylayout.group, self.GROUP)
        self.assertEqual(keylayout.id_, self.ID)
        self.assertEqual(keylayout.name, self.NAME)
        self.assertEqual(keylayout.maxout, self.MAXOUT)
        self.assertEqual(keylayout.default_index, 0)

    def test_keylayout_init_without_maxout(self):
        spec = self.spec.copy()
        del spec['maxout']
        keylayout = self.keylayout_factory.from_spec(spec)

        self.assertEqual(keylayout.group, self.GROUP)
        self.assertEqual(keylayout.id_, self.ID)
        self.assertEqual(keylayout.name, self.NAME)
        self.assertEqual(keylayout.maxout, 1)
        self.assertEqual(keylayout.default_index, self.DEFAULT_INDEX)

    def test_keylayout_str(self):
        expected = f'Keylayout({self.NAME}, (id: {self.ID}))'
        actual = str(self.keylayout)

        self.assertEqual(expected, actual)

    def test_keyboard_attributes(self):
        expected = {
            'group':  str(self.GROUP),
            'id':     str(self.ID),
            'name':   str(self.NAME),
            'maxout': str(self.MAXOUT),
        }
        actual = self.keylayout.keyboard_attributes()

        self.assertEqual(expected, actual)

    def test_layouts_converted_to_str(self):
        # TODO: Mock Keylayout object creation.
        layouts = {
            'int_val': 1,
            'str_val': 'value',
        }

        spec = {
            'key_map': None,
            'key_map_select': None,
            'layouts': layouts,
        }

        keylayout = self.keylayout_factory.from_dict(spec)

        self.assertEqual(keylayout.layouts, [convert_items_to_str(layouts)])


class TestIsoKeylayout(TestKeylayout):
    __test__ = True

    def setUp(self):
        self._setUp('iso')


class TestIsoDvorakKeylayout(TestKeylayout):
    __test__ = True

    def setUp(self):
        self._setUp('iso_dvorak')

# TODO: iso_jdvorak


if __name__ == '__main__':
    unittest_main()

