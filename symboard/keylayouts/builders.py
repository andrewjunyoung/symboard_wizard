"""
.. module:: keylayouts
   :synopsis: Builder class(es) to convert a dict into a Keylayout instance.

.. moduleauthor:: Andrew J. Young

"""


# Imports from third party packages.
from sys import modules

# Imports from this package.
from symboard.errors import SpecificationException
from symboard.keylayouts.ansi_keylayout import AnsiKeylayout
from symboard.keylayouts.iso_keylayout import IsoKeylayout
from symboard.keylayouts.keylayouts import Keylayout
from symboard.yaml_spec import OPTIONAL_PROPERTIES, NAME_TO_KEYLAYOUT_CLASS_MAP


def _filter_none_elems_from_map(map_: map):
    """ Given a map (call it m), returns a new map which contains all the
    non-null (non-none) elements of m.

    Args:
        map_: The map to return the non-null elements of.

    Returns:
        A new map with all the non-null elements of <map_>.
    """
    return {k: v for k, v in map_.items() if v is not None}


def keylayout_from_spec(spec: dict):
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
        # Keylayout class to init.
        keylayout_class = _class_from_base_keylayout(spec['base_layout'])

        # Non optional init arguments.
        id_ = spec['id']
        group = spec['group']

        # Optional init arguments.
        optional_kwargs = {
            key: spec.get(key, None) for key in OPTIONAL_PROPERTIES
        }
        kwargs = _filter_none_elems_from_map(optional_kwargs)

        return keylayout_class(group, id_, **kwargs)
    except:
        raise SpecificationException()


def _class_from_base_keylayout(base_keylayout: str) ->  Keylayout:
    """
    Args:
        base_keylayout (str): The name of the base_keylayout to use.

    Returns:
        Keylayout: The keylayout class (which inherits from Keylayout) that is
            described by <base_keylayout>.

    Raises:
        SpecificationException: If <base_keylayout> does not have a valid
            reference to a Keylayout class (defined by the Symboard language
            spec.
    """

    # This is much faster than checking if base_keylayout is an elem.
    try:
        return globals()[NAME_TO_KEYLAYOUT_CLASS_MAP[base_keylayout]]
    except:
        raise SpecificationException()#'base_keylayout', base_keyboard)

