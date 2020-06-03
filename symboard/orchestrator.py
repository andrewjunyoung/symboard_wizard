"""
.. module:: orchestrator
   :synopsis: A file describing the orchestrator, a class which manages the
   execution and program flow of the Symboard compiler.

.. moduleauthor:: Andrew J. Young

"""

# Imports from third party packages.
import logging

# Imports from the local package.
from symboard.file_writers import KeylayoutXMLFileWriter
from symboard.parsers import YamlFileParser
from symboard.keylayouts import KeylayoutFactory
from symboard.states import load_yaml


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
        logging.info(f'Parsing the contents from {input_path}.')

        keylayout_spec = YamlFileParser.parse(
            input_path, case_sensitive = True,
        )

        logging.info(f'Importing states from the states directory.')

        states = load_yaml()

        logging.info(f'Creating the keyboard object from the specification.')

        keylayout_factory = KeylayoutFactory()
        keylayout = keylayout_factory.from_spec(keylayout_spec)

        logging.info(f'Trying to write the keylayout to disk at {output_path}.')

        file_writer = KeylayoutXMLFileWriter()
        file_writer.write(keylayout, output_path)

