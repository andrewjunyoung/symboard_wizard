"""
.. module:: keylayouts
   :synopsis: Builder class(es) to convert a dict into a Keylayout instance.

.. moduleauthor:: Andrew J. Young

"""


# Imports from this package.
from symboard.keylayouts.ansi_keylayout import (
    Keylayout,
    AnsiKeylayout,
)
from symboard.errors import SpecificationException # TODO: define this.


NAME_TO_KEYLAYOUT_CLASS_MAP = {
    'ansi': AnsiKeylayout,
}


def get_keylayout_from_spec(spec: dict) -> Keylayout:
    """ Given a dictionary with the specifications (specs) of a keyboard, tries
    to create a keylayout class meeting these specs.

    Args:
        spec (dict): The full spec of the desired keylayout.

    Returns:
        keylayout: The keylayout meeting the full spec.

    Raises:
        SpecificationException: If the spec cannot be met in its entirety or is
            malformed.
    """

    try:
        # Mandatory values.
        _get_class_from_base_keyboard(spec['base_keyboard'])
        id_ = spec['id']
        group = spec['group']

        # Optional values.
        maxout = spec.get('maxout', None)
        name = spec.get('name', None)
        default_index = spec.get('default_index', None)
    except:
        raise SpecificationException()


def _get_class_from_base_keyboard(base_keyboard: str) ->  Keylayout:
    """
    Args:
        base_keyboard (str): The name of the base_keyboard to use.

    Returns:
        Keylayout: The keylayout described by the base keyboard.

    Raises:
        SpecificationException: If <base_keyboard> does not have a valid
            reference to a Keylayout class (defined by the Symboard language
            spec.
    """

    # This is much faster than checking if base_keyboard is an elem.
    try:
        return NAME_TO_KEYLAYOUT_CLASS_MAP[base_keyboard]
    except:
        raise SpecificationException('base_keyboard', base_keyboard)

