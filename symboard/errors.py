'''
@author Andrew J. Young
@description The custom error classes used by symboard.
'''

class BaseSymboardException(BaseException):
    def __init__(self, msg: str = ''):
        self.msg = msg


class ParserException(BaseSymboardException):
    def __init__(self, msg: str = ''):
        super(ParserException, self).__init__(msg)


class WriteException(BaseSymboardException):
    def __init__(self, msg: str = ''):
        super(WriteException, self).__init__(msg)

