'''
@author: Andrew J. Young
@description: A file describing the orchestrator, a class which manages the
              execution and program flow of the Symboard compiler.
'''

from file_writer.KeylayoutFileWriter import KeylayoutFileWriter
from parsers.YamlParser import YamlFileParser

class Orchestrator:

    def run(self, input_file_path: str, output_file_path: str) -> None:
        # Parse the input from <input_file_path>
        keylayout_info_dict = YamlFileParser.parse(input_file_path)

        # Write the keylayout to a file
        symboard_file_writer = KeylayoutFileWriter()
        symboard_file_writer.write(output_file_path)

