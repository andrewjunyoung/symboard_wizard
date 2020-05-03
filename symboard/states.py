"""
.. module:: keylayouts
   :synopsis: A collection of functions to load states into memory so that they
   can be used by keylayouts.

.. moduleauthor:: Andrew J. Young

"""


# Imports from the standard library.
from os import walk

# Imports from third party packages.
#from mypy import Dict
from yaml import safe_load

# Imports from this package.
from symboard.actions import State


states_dir = 'symboard/states'
""" The relative path to the directory containing definitions of states. These
states can be pre-defined by the Symboard project, or added by users.
"""


def load_yaml():
    """ Loads all yaml files which can be found in the folder <states_dir>, and
    adds them to an object «states», which can then be imported and used
    throughout the project.
    """
    states: Dict[State] = {}

    for _, _, file_names in walk(states_dir):
        for file_name in file_names:
            file_path = states_dir + '/' + file_name

            with open(file_path, 'r') as file_:
                contents = safe_load(file_)

            for name, attribs in contents.items():
                states[name] = State(
                    name=name,
                    terminator=attribs['terminator'],
                ).with_lower(
                    attribs['lower']
                )

    return states


states = load_yaml()
""" An object containing all states found inside <states_dir>, which can be
imported and used throughout the project.
"""

