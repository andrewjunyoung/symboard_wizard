'''
@author Andrew J. Young
@description The custom error classes used by symboard.
'''

class BaseSymboardException(BaseException):
    def __init__(self, msg: str = ''):
        self.msg = msg


class ParserException(BaseSymboardException):
    pass


class WriteException(BaseSymboardException):
    pass


class FileExistsException(WriteException):
    pass


class NoneException(BaseSymboardException):
    pass


class ContentsNoneException(NoneException):
    pass
