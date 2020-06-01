def filter_none_elems_from_dict(dict_: dict) -> dict:
    """ Given a dict (call it d), returns a new dict which contains all the
    non-null (non-none) elements of d.

    Args:
        dict_: The dict to return the non-null elements of.

    Returns:
        A new dict with all the non-null elements of <dict_>.
    """
    return {k: v for k, v in dict_.items() if v is not None}


def convert_items_to_str(dict_: dict) -> dict:
    """ Given a dict (call it d), returns a new dict which contains all the
    elements of d cast to str.

    Args:
        dict_: The dict to cast the key-value pairs of.

    Returns:
        A new dict with all keys and values of <dict_> but cast to strings.
    """
    return {str(k): str(v) for k, v in dict_.items()}
