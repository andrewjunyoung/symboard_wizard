'''
@author: Andrew J. Young
@description: A series of classes which describe classes about keyboards which
are intended not be used on their own, but instead to be inherited from.
'''

# Imports from third party packages.
from mypy import Dict


class Keylayout:
    name: str = ''
    language: str = ''
    key_map: Dict[int, str] = {}

    def __str__(self):
        print('Keylayout(${name}, ${language})'.format())

