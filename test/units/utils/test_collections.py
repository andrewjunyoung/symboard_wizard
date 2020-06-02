from unittest import TestCase
from unittest import main as unittest_main

# Local package imports.
from symboard.utils.collections import (
    filter_none_elems_from_dict,
    convert_items_to_str,
)


class TestCollectionsUtils(TestCase):
    def _test_convert_items_to_str(self, input_, expected_output):
        actual_output = convert_items_to_str(input_)
        self.assertEqual(expected_output, actual_output)

    def test_convert_items_to_str(self):
        test_cases = [
            ({}, {}),
            ({1: 2}, {'1': '2'}),
            ({'1': 2}, {'1': '2'}),
            ({1: '2'}, {'1': '2'}),
            ({1: '2', '3': 4}, {'1': '2', '3': '4'}),
        ]

        for input_, expected_output in test_cases:
            self._test_convert_items_to_str(input_, expected_output)

    def _test_filter_none_elems_from_dict(self, input_, expected_output):
        actual_output = filter_none_elems_from_dict(input_)
        self.assertEqual(expected_output, actual_output)

    def test_filter_none_elems_from_dict(self):
        test_cases = [
            ({}, {}),
            ({'a': 'A'}, {'a': 'A'}),
            ({'a': 'A', 'b': None}, {'a': 'A'}),
            ({'a': None, 'b': None}, {}),
            ({'a': None}, {}),
            ({'a': 'A', 'b': 'B'}, {'a': 'A', 'b': 'B'}),
        ]

        for input_, expected_output in test_cases:
            self._test_filter_none_elems_from_dict(input_, expected_output)


if __name__ == '__main__':
    unittest_main
