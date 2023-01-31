"""Stub Reader to get initial testing and CI off the ground."""
from typing import Union


def get(path: str, parsed_dict: dict) -> Union[None, dict, tuple, list, str, int]:
    """Getter that is used to look up the single/section value(s) in the parsed
    config from a supplied dot path.

    :param str path: Dot notation path into the parsed config. eg.
        "key1.subkey7".
    :param dict parsed_dict: Dict to do a lookup against.
    :returns: The value of the key, whether it is a single value or a section.
    """
    _keys = path.split(".")
    cmd_str = "parsed_dict"
    for _key in _keys:
        cmd_str += f".get('{_key}', {{}})"

    # FIXME: #7 Remove this dirty, high-risk implementation with `eval()`. I'm
    # trying it for a quick way to convert a dotted-path to a dictionary
    # lookup, but it can lead to potential abuse from un-validated, malformed
    # strings passed in by the User.
    ret_val = eval(cmd_str)
    return ret_val
