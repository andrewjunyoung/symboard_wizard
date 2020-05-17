from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch
from unittest import main as unittest_main
from scripts.show_states import main, format_outputs


show_states_path = 'scripts/show_states.py'


class TestShowStates(TestCase):
    def setUp(self):
        self.outputs = ['a','b','c','d','e','f','g']
        attrs = {'action_to_output_map.values.return_value': self.outputs}

        self.state_name = 'state_name'
        self.state_terminator = '.'

        self.state = MagicMock(
            name = self.state_name,
            terminator = self.state_terminator,
            **attrs
        )

    def test_format_outputs(self):
        expected = ''.join(self.outputs)
        actual = format_outputs(self.state)

        self.assertEqual(expected, actual)

    @patch(show_states_path + '.load_yaml')
    def test_main(self, load_yaml):
        # Setup.
        expected_headers = ['Name', 'Terminator', 'Outputs']
        expected_output = tabulate(
            data, headers=expected_headers, tablefmt='orgtbl'
        )

        load_yaml.return_value = {self.state_name: self.state}

        # Execution.
        main()

        # Assertion.
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest_main()
