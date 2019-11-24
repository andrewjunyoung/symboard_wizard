'''
@author: Andrew J. Young
@description: A collection of parsers which are designed not to be used on their
own, but instead to be inherited from and extended from.
'''

# Package internal imports
from symboard.errors import ParserException

# Third party imports
from yaml import safe_load
from typing import Dict
from os.path import isfile


class Parser:
    @staticmethod
    def parse(content):
        pass


class StringParser(Parser):
    @staticmethod
    def parse(content: str):
        pass


class FileParser(Parser):
    @staticmethod
    def parse(file_path: str):
        pass


class YamlFileParser(FileParser):
    @staticmethod
    def parse(file_path: str) -> Dict:
        try:
            if not isfile(file_path):
                raise ParserException('''Parser error: The path «{}» does not
                exist or is not a file.'''.format(file_path))

            with open(file_path, 'r') as stream:
                return safe_load(stream)
        except:
            raise ParserException('''Parser error: Could not read file contents
            from «{}»'''.format(file_path))

