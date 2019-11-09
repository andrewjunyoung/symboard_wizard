'''
@author: Andrew J. Young
@description: A yaml parser which converts any yaml into a python readable data
object.
'''

# Internal imports
from parsers.base_parsers import StringParser

# Third party imports
from yaml import load
from mypy import Dict


class YamlFileParser(FileParser):
    def parse(self, file_path: str) -> Dict:
        _file = open(file_path, 'r')
        contents: str = _file.read()
        _file.close()
        return yaml.load(contents)

