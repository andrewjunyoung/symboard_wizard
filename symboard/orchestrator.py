"""
.. module:: orchestrator
   :synopsis: A file describing the orchestrator, a class which manages the
   execution and program flow of the Symboard compiler.

.. moduleauthor:: Andrew J. Young

"""

from symboard.file_writers import KeylayoutXMLFileWriter
from symboard.parsers import YamlFileParser
from symboard.keylayouts.builders import keylayout_from_spec


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
        # Parse the contents from <input_path>.
        keylayout_spec = YamlFileParser.parse(
            input_path, case_sensitive = True,
        )
        # Create the keyboard object from the specification.
        keylayout = keylayout_from_spec(keylayout_spec)

        # Write the keylayout to a file
        file_writer = KeylayoutXMLFileWriter()
        file_writer.write(keylayout, output_path)

