'''
@author: Andrew J. Young
@description: A collection of parsers which are designed not to be used on their
own, but instead to be inherited from and extended from.
'''

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
