"""

.. module:: keylayouts
   :synopsis: A collection of functions to load states into memory so that they
   can be used by keylayouts.

.. moduleauthor:: Andrew J. Young

"""


# Imports from the standard library.
from os import walk
import logging

# Imports from third party packages.
from yaml import safe_load

# Imports from this package.
from symboard.actions import State
from settings import STATE_ATTRIBUTE_PRECEDENCE, STATES_DIR


def load_yaml():
    """ Loads all yaml files which can be found in the folder <STATES_DIR>, and
    adds them to an object «states», which can then be imported and used
    throughout the project.
    """
    logging.info(
        f'Creating yaml states object using files from folder «{STATES_DIR}».'
    )

    states: Dict[State] = {}

    for _, _, file_names in walk(STATES_DIR):
        for file_name in file_names:
            logging.info(f'Importing yaml states from file {file_name}.')

            file_path = STATES_DIR + '/' + file_name

            with open(file_path, 'r') as file_:
                contents = safe_load(file_)

            for name, attribs in contents.items():
                new_state = State(
                    name=name,
                    # Using .get allows us to pass in a None argument without
                    # raising an error.
                    terminator=attribs.get('terminator'),
                )

                for attrib in STATE_ATTRIBUTE_PRECEDENCE:
                    if attribs.get(attrib):
                        method = new_state.builder_method_from_attrib_name(
                            attrib
                        )
                        new_state = method(attribs[attrib])

                states[name] = new_state

    return states


states = load_yaml()
""" An object containing all states found inside <STATES_DIR>, which can be
imported and used throughout the project.
"""

