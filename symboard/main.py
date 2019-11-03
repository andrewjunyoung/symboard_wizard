'''
@author: Andrew J. Young
@description: The entry point for the symboard executable when run on the
command line.
'''

from orchestrator.Orchestrator import Orchestrator
from argparse import ArgumentParser

def get_parser() -> ArgumentParser:
    # TODO: Should be in factory
    parser = ArgumentParser(description='''
    Create a ".keylayout" file from a ".symboard" file.
    ''')

    parser.add_argument('input_file_path', type=str, nargs=1,
            help='''The file path of the .symboard file which you want to make a
            keyboard layout from.''',)
    parser.add_argument('output_file_path', type=str, nargs='?',
            default='./a.keylayout',
            help='''The file path for where you want to save the .keylayout that
            symboard creates.''',)

    return parser


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()

    orchestrator = Orchestrator()
    orchestrator.run(args.output_file_path)

if __name__ == '__main__':
    # Parse command line args.
   main()
