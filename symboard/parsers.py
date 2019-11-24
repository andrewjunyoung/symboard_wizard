'''
@author: Andrew J. Young
@description: A collection of parsers which are designed not to be used on their
own, but instead to be inherited from and extended from.
'''

# Third party imports
from yaml import safe_load
from typing import Dict


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
        with open(file_path, 'r') as stream:
            return safe_load(stream)
