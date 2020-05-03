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


class NotAFileException(ParserException):
    """ Indicates that the file to be parsed does not exist or is not a file.
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

class SpecificationException(BaseSymboardException):
    """ Indicates that something has gone wrong when trying to create a keyboard
    that meets the specification defined by the user.
    """
    pass

class AlphabetLengthException(BaseSymboardException):
    """ Indicates that the alphabet provided has the wrong number of letters (it
    should have 26).
    """
    def __init__(self, alphabet):
        super().__init__(msg=f'Alphabet {alphabet} of length {len(alphabet)} is'
        'not a valid alphabet length.')

class CouldNotGetOutputException(BaseSymboardException):
    """ Indicates that the object does not have a well defined output that can
    be used when a key is pressed.
    """
    def __init__(self, object_):
        super().__init__(
            msg=f'could not find an output field in object_.object_ is of type'
            '{type(object_)}, but should be of type str or'
            'Action.'
        )

