"""Stub Reader to get initial testing and CI off the ground."""
from typing import Union


def get(path: str) -> Union[None, dict, tuple, list, str, int]:
    """Getter that is used to look up the single/section value(s) in the parsed
    config from a supplied dot path.

    :param str path: Dot notation path into the parsed config. eg.
        "key1.subkey7".
    :returns: The value of the key, whether it is a single value or a section.
    """
    return None
