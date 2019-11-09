'''
@author: Andrew J. Young
@description: A file describing the orchestrator, a class which manages the
              execution and program flow of the Symboard compiler.
'''

from file_writer.KeylayoutFileWriter import KeylayoutFileWriter

class Orchestrator:

    def run(self, output_file_path: str) -> None:
        symboard_file_writer = KeylayoutFileWriter()
        symboard_file_writer.write(output_file_path)

