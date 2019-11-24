'''
@author: Andrew J. Young
@description: A file writer, which given input will output this as formatted
data to a specified output file.
'''

# Package internal imports
from symboard.errors import WriteException

# Third party package imports
from os.path import exists


DEFAULT_OUTPUT_FILE_PATH = './a.keylayout'


class FileWriter:

    def write(self):
        pass


class KeylayoutFileWriter(FileWriter):

    @staticmethod
    def write(output_file_path: str = DEFAULT_OUTPUT_FILE_PATH) -> None:
        ''' Given an output file path, creates a file in that file path.
        Assumes the file is not already present. Throws an error if this
        is not true.
        '''

        if exists(output_file_path):
            raise WriteException()

        with open(output_file_path, 'w+') as f:
            # TODO
            pass

