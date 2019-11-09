'''
@author: Andrew J. Young
@description: A collection of parsers which are designed not to be used on their
own, but instead to be inherited from and extended from.
'''

class Parser:
    def parse(self, content):
        pass


class StringParser(Parser):
    def parse(self, content: str):
        pass


class FileParser(Parser):
    def parse(self, file_path: str):
        pass
