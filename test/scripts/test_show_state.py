# From third party packages.
from io import StringIO
from tabulate import tabulate
from unittest import TestCase
from unittest import main as unittest_main
from unittest.mock import MagicMock, mock_open, patch, PropertyMock

# From the local package.
from scripts.show_states import main, format_outputs


show_states_path = 'scripts.show_states'


class TestShowStates(TestCase):
    def setUp(self):
        self.output_list = ['a','b','c','d','e','f','g']
        self.outputs = ''.join(self.output_list)
        attrs = {'action_to_output_map.values.return_value': self.output_list}

        self.state_name = 'state_name'
        self.state_terminator = '.'

        # MagicMock has issues mocking the property «name» because it uses this
        # keyword argument in its own initialization function. The below is a
        # workaround.
        name = PropertyMock(return_value=self.state_name)
        self.state = MagicMock(
            terminator = self.state_terminator,
            **attrs
        )
        type(self.state).name = name

    def test_format_outputs(self):
        actual = format_outputs(self.state)
        self.assertEqual(self.outputs, actual)

    @patch(show_states_path + '.tabulate')
    @patch(show_states_path + '.load_yaml')
    def test_main(self, load_yaml, tabulate):
        # Setup.
        data = [
            [self.state_name, self.state_terminator, self.outputs]
        ]
        expected_headers = ['Name', 'Terminator', 'Outputs']

        output_string = 'output'
        expected_output = output_string + '\n'

        load_yaml.return_value = {self.state_name: self.state}
        tabulate.return_value = output_string

        with patch('sys.stdout', new = StringIO()) as fake_out:
            # Execution.
            main()

            # Assertion.
            self.assertEqual(expected_output, fake_out.getvalue())
            tabulate.assert_called_once_with(
                data,
                headers=expected_headers,
                tablefmt='orgtbl'
            )


if __name__ == '__main__':
    unittest_main()

