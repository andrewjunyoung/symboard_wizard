"""
.. module:: parsers
   :synopsis: A collection of parsers which are designed not to be used on their
   own, but instead to be inherited from and extended from.

.. moduleauthor:: Andrew J. Young

"""

# Imports from third party packages.
from yaml import safe_load
from typing import Dict, Any
from os.path import isfile

# Package internal imports
from symboard.errors import ParserException, NotAFileException


class Parser:
    """ A generic implementation of a parser which should be inherited from. It
    contains one method («parse») which should be overwritten by children of
    this class.
    """
    @staticmethod
    def parse(content):
        """ A generic implementation of parsing which should be overwritten by
        children of this class.

        Args:
            content (object): The content to parse.
        """
        pass


class StringParser(Parser):
    """ A generic implementation of a string parser which should be inherited
    from. It contains one method, «parse», which should be overwritten by
    children of this class.
    """
    @staticmethod
    def parse(content: str):
        """ A generic implementation of string parsing which should be
        overwritten by children of this class.

        Args:
            content (str): The string to parse.
        """
        pass


class FileParser(Parser):
    """ A generic implementation of a file parser which should be inherited
    from. It contains one method, «parse», which should be overwritten by
    children of this class.
    """
    @staticmethod
    def parse(file_path: str):
        """ A generic implementation of file parsing which should be
        overwritten by children of this class.

        Args:
            file_path (str): The path of the file to parse.
        """
        pass


class YamlFileParser(FileParser):
    """ A file parser which parses yaml files, using the method «parse» as the
    exposed API function for parsing.
    """

    @staticmethod
    def _try_lower(obj: object) -> object:
        try:
            return obj.lower()
        except:
            return obj

    @staticmethod
    def _lower_dict(dict_: Dict[str, Any]) -> Dict[str, Any]:
        return {k.lower(): YamlFileParser._try_lower(v)
            for k, v in dict_.items()
        }

    @staticmethod
    def parse(file_path: str, case_sensitive: bool = True) -> Dict:
        """ An implementation of parsing yaml files.

        Args:
            file_path (str): The path of the yaml file to parse.

        Returns:
            Dict: A dictionary containing the parsed data contained by the
                specified yaml file.

        Raises:
            ParserException: If the path does not exist or is not a file; or if
            some other error occurs.
        """

        try:
            if not isfile(file_path):
                raise NotAFileException('''Parser error: The path «{}» does not
                exist or is not a file.'''.format(file_path))

            with open(file_path, 'r') as stream:
                parsed_dict = safe_load(stream)

            if not case_sensitive:
                parsed_dict = YamlFileParser._lower_dict(parsed_dict)

            return parsed_dict

        except:
            raise ParserException('''Parser error: Could not read file contents
            from «{}»'''.format(file_path))

