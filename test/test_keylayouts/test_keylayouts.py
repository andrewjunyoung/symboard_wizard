# Imports from third party packages.
from unittest import TestCase
from unittest import main as unittest_main

# Imports from the local package.
from symboard.keylayouts.keylayouts import Keylayout


class TestKeylayout(TestCase):
    def setUp(self):
        self.GROUP = 1
        self.ID = 2
        self.NAME = '3'
        self.MAXOUT = 4
        self.DEFAULT_INDEX = 5

        self.class_ = Keylayout
        self.keylayout = Keylayout(
            self.GROUP,
            self.ID,
            maxout = self.MAXOUT,
            name = self.NAME,
            default_index = self.DEFAULT_INDEX,
        )

    def test_keylayout_init_with_all_properties_provided(self):
        keylayout = self.keylayout

        self.assertEqual(keylayout.group, self.GROUP)
        self.assertEqual(keylayout.id_, self.ID)
        self.assertEqual(keylayout.name, self.NAME)
        self.assertEqual(keylayout.maxout, self.MAXOUT)
        self.assertEqual(keylayout.default_index, self.DEFAULT_INDEX)

    def test_keylayout_init_without_default_index(self):
        keylayout = Keylayout(
            self.GROUP, self.ID,
            maxout = self.MAXOUT, name = self.NAME
        )

        self.assertEqual(keylayout.group, self.GROUP)
        self.assertEqual(keylayout.id_, self.ID)
        self.assertEqual(keylayout.name, self.NAME)
        self.assertEqual(keylayout.maxout, self.MAXOUT)
        self.assertEqual(keylayout.default_index, 0)

    def test_keylayout_init_without_maxout(self):
        keylayout = Keylayout(
            self.GROUP, self.ID,
            name = self.NAME, default_index = self.DEFAULT_INDEX
        )

        self.assertEqual(keylayout.group, self.GROUP)
        self.assertEqual(keylayout.id_, self.ID)
        self.assertEqual(keylayout.name, self.NAME)
        self.assertEqual(keylayout.maxout, 1)
        self.assertEqual(keylayout.default_index, self.DEFAULT_INDEX)

    def test_default_name_is_as_defined_in_the_class(self):
        keylayout = self.class_(self.GROUP, self.ID, self.MAXOUT)

        self.assertEqual(keylayout.name, self.class_._DEFAULT_NAME)

    def test_keylayout_str(self):
        expected = 'Keylayout({}, (id: {}))'.format(self.NAME, self.ID)
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

if __name__ == '__main__':
    unittest_main()

