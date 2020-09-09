# Imports from third party packages.
from argparse import ArgumentParser
from tabulate import tabulate
from typing import List
import logging

# Imports from the local package.
from symboard.states import load_yaml


def get_arg_parser() -> ArgumentParser:
    """
    Returns:
        ArgumentParser: An ArgumentParser instance which will parse the
            arguments provided to Symboard when executed from the command line.
    """
    parser = ArgumentParser(
        description='Show all the states available to your program inside the' \
        'states directory, and some info about each of these states.'
    )

    return parser


def format_outputs(state):
    """
    Returns:
        str: A concatenated list of all of the outputs in the given state's
        action_to_output_map.
    """
    return ''.join(state.action_to_output_map.values())


def main() -> None:
    """ The main method (entry point) for the script. This function parses the
    input arguments, and manages the core code logic using these arguments.
    """
    logging.info(f'Parsing command line arguments.')

    arg_parser: ArgumentParser = get_arg_parser()
    args = arg_parser.parse_args()

    logging.info(f'Collecting states from states directory.')

    states: dict = load_yaml()

    headers: List[str] = ['Name', 'Terminator', 'Outputs']
    data: List[list] = [
        [state.name, state.terminator, format_outputs(state)]
        for state in states.values()
    ]

    print(tabulate(data, headers=headers, tablefmt='orgtbl'))


if __name__ == '__main__':
    main()

