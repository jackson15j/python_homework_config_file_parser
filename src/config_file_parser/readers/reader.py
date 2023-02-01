"""Stub Reader to get initial testing and CI off the ground."""
from typing import Union


def _to_str(item: Union[str, bytes]) -> str:
    """Decode to str helper to get around `mypy` type noise in upstream
    str-only functions."""
    if isinstance(item, bytes):
        # Handle RFC7159/JSON-spec which allows Full Stops to be used in the key
        return item.decode("utf-8")
    return item


def get(
    path: Union[str, bytes], parsed_dict: dict
) -> Union[None, dict, tuple, list, str, int]:
    """Getter that is used to look up the single/section value(s) in the parsed
    config from a supplied dot path.

    :param str|bytes path: Dot notation path into the parsed config.
        eg. "key1.subkey7".
        NOTE: `path` must be a bytes object to allow passing `\u002e` to do
        look-ups of a key containing a full stop!
        eg. Key = "a.b", send: `b"a\u002eb"`.
    :param dict parsed_dict: Dict to do a lookup against.
    :returns: The value of the key, whether it is a single value or a section.
    """
    _path: str = _to_str(path)
    _keys = _path.split(".")
    cmd_str = "parsed_dict"
    for _key in _keys:
        cmd_str += f".get('{_key}', {{}})"

    # FIXME: #7 Remove this dirty, high-risk implementation with `eval()`. I'm
    # trying it for a quick way to convert a dotted-path to a dictionary
    # lookup, but it can lead to potential abuse from un-validated, malformed
    # strings passed in by the User.
    ret_val = eval(cmd_str)
    return ret_val
