"""
.. module:: orchestrator
   :synopsis: A file describing the orchestrator, a class which manages the
   execution and program flow of the Symboard compiler.

.. moduleauthor:: Andrew J. Young

"""

from symboard.file_writers import KeylayoutFileWriter
from symboard.parsers import YamlFileParser

class Orchestrator:
    """ A class which defines one method («run»). This method defines and
    controls the execution of Symboard given the parameters with which Symboard
    was called.
    """
    def run(self, input_path: str, output_path: str) -> None:
        """ This method defines and controls the execution of Symboard given the
        parameters with which Symboard was called. it will parse the given input
        file, create a keylayout according to that spec, and write this
        keylayout as an XML file to the specified output path.

        Args:
            input_path (str): The path to the file containing the specification
                from which to create a keylayout.
            output_path (str): The path to which the output keylayout is to be
                written.
        """
        # Parse the input from <input_>
        keylayout_info_dict = YamlFileParser.parse(input_path)

        # Write the keylayout to a file
        symboard_= KeylayoutFileWriter()
        # TODO: Fix
        #symboard_.write(Keyl, output_path)

