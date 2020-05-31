def filter_none_elems_from_dict(dict_: dict):
    """ Given a dict (call it m), returns a new dict which contains all the
    non-null (non-none) elements of m.

    Args:
        dict_: The dict to return the non-null elements of.

    Returns:
        A new dict with all the non-null elements of <dict_>.
    """
    return {k: v for k, v in dict_.items() if v is not None}
