'''
@author: Andrew J. Young
@description: A file writer, which given input will output this as formatted
data to a specified output file.
'''

class FileWriter:

    def write(self):
        pass


class KeylayoutFileWriter(FileWriter):

    def write(
            self,
            output_file_path: str = './a.keylayout',
            ) -> None:
        ''' Given an output file path, creates a file in that file path.
        Assumes the file is not already present. Undetermined behavior if this
        is not true.
        '''
        _file = open(output_file_path, 'w+')
        _file.close()

        pass
