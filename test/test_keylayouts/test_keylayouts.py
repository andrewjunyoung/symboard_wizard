# Imports from third party packages.
from unittest import TestCase
from unittest import main as unittest_main


class TestKeylayout(TestCase):
    def setup(self):
        self.GROUP = 1
        self.ID = 2
        self.NAME = '3'
        self.MAXOUT = 4
        self.DEFAULT_INDEX = 5

        self.keylayout = Keylayout(
            self.GROUP,
            self.ID,
            self.NAME,
            self.MAXOUT,
            self.DEFAULT_INDEX
        )

    def test_keylayout_init(self):
        keylayout = self.keylayout

        self.assertEqual(keylayout.group, self.GROUP)
        self.assertEqual(keylayout.id_, self.ID)
        self.assertEqual(keylayout.name, self.NAME)
        self.assertEqual(keylayout.maxout, self.MAXOUT)

    def test_keylayout_str(self):
        expected = 'Keylayout({}, (id: {}))'.format(self.NAME, self.ID)
        actual = str(self.keylayout)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest_main()

