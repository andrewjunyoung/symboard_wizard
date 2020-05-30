"""
.. module:: keylayouts
   :synopsis: Builder class(es) to convert a dict into a Keylayout instance.

.. moduleauthor:: Andrew J. Young

"""


# Imports from third party packages.
from sys import modules
import logging

# Imports from this package.
from symboard.errors import SpecificationException
from symboard.yaml_spec import OPTIONAL_PROPERTIES
from symboard.parsers import YamlFileParser
from settings import KEYLAYOUTS_DIR, KEYLAYOUTS_FILE_SUFFIX


def _filter_none_elems_from_dict(dict_: dict):
    """ Given a dict (call it m), returns a new dict which contains all the
    non-null (non-none) elements of m.

    Args:
        dict_: The dict to return the non-null elements of.

    Returns:
        A new dict with all the non-null elements of <dict_>.
    """
    return {k: v for k, v in dict_.items() if v is not None}


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

    # Get a base class instance
    keylayout_base = _class_from_base_keylayout(spec['base_layout'])

    # Non optional init arguments.
    keylayout_base.id_ = spec['id']
    keylayout.group = spec['group']

    # TODO: Optional init arguments.
    #optional_kwargs = {
    #    key: spec.get(key, None) for key in OPTIONAL_PROPERTIES
    #}
    #kwargs = _filter_none_elems_from_dict(optional_kwargs)


def _class_from_base_keylayout(base_keylayout: str):
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

    file_path = f'{KEYLAYOUTS_DIR}/{base_keylayout}.{KEYLAYOUTS_FILE_SUFFIX}'

    spec = YamlFileParser.parse(file_path)

    logging.info(f'here: {spec}')

    return KeylayoutFactory.from_dict(spec)

