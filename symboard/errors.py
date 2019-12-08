"""
.. module:: errors
   :synopsis: The custom error classes used by symboard.

.. moduleauthor Andrew J. Young

"""

class BaseSymboardException(BaseException):
    """ A generic exception which can be thrown when some other exception does
    not accurately describe the problem, and should be inherited from by all
    other exceptions used by the Symboard program.
    """
    def __init__(self, msg: str = ''):
        self.msg = msg


class ParserException(BaseSymboardException):
    """ Indicates that something has gone wrong when parsing.
    """
    pass


class WriteException(BaseSymboardException):
    """ Indicates that something has gone wrong when writing to file.
    """
    pass


class FileExistsException(WriteException):
    """ Indicates that the file to be written to already exists, and so cannot
    be written to.
    """
    pass


class NoneException(BaseSymboardException):
    """ Indicates that one of the variables in the program is None, but was
    expected not to be.
    """
    pass


class KeylayoutNoneException(NoneException):
    """ Indicates a keylayout is None, but was expected not to be.
    """
    pass
