# Imports from third party packages.
from argparse import ArgumentParser
from os import system
import logging


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

    parser.add_argument(
        'input_path',
        help='the keylayout file to install to the system',
    )

    return parser


def main() -> None:
    """ The main method (entry point) for the script. This function parses the
    input arguments, and manages the core code logic using these arguments.
    """
    logging.info(f'Parsing command line arguments.')

    arg_parser: ArgumentParser = get_arg_parser()
    args = arg_parser.parse_args()

    logging.info(f'Copying file to the keylayouts directory.')

    input_path = args.input_path
    output_path = '/Library/Keyboard\ Layouts'


    system(f'sudo cp {input_path} {output_path}')

    logging.info(
        f'Done! Your keyboard is now be available to use on your operating system.'
    )

if __name__ == '__main__':
    main()
