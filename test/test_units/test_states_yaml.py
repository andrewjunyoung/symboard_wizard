# Imports from third party packages.
from unittest import TestCase
from unittest import main as unittest_main

# Imports from the local package.
from symboard.states import states


class TestStatesYaml(TestCase):
    def test_states_load(self):
        # Test that all states load correctly.
        states

    def test_states_are_well_formed(self):
        for state_name in states.keys():
            self.assertIsNotNone(states[state_name].name)
            self.assertIsNotNone(states[state_name].terminator)
            self.assertIsNotNone(states[state_name].action_to_output_map)


if __name__ == '__main__':
    unittest_main()
