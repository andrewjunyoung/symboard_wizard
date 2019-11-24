'''
@author: Andrew J. Young
@description: A yaml parser which converts any yaml into a python readable data
object.
'''

# Internal imports
from parsers.base_parsers import FileParser

# Third party imports
from yaml import safe_load
from typing import Dict


class YamlFileParser(FileParser):
    @staticmethod
    def parse(file_path: str) -> Dict:
        with open(file_path, 'r') as stream:
            return safe_load(stream)

