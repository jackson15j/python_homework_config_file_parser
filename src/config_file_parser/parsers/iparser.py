"""Interface that all Parser's inherit."""

from abc import ABC, abstractmethod



class FileNotFound(Exception):
    """File not found exception."""


class ParseException(Exception):
    """Failed to parse content exception."""


class IParser(ABC):
    """Base Parser."""

    def __init__(self):
        self._files: list = []
        self._parsed_files: list = []
        self._parsed_dict: dict = {}

    @property
    def files(self) -> list:
        """Returns list of supplied files to parse."""
        return self._files

    @property
    def parsed_files(self) -> list:
        """Returns list of files that were parsed."""
        return self._parsed_files

    @property
    def parsed_dict(self) -> dict:
        """Returns Dict containing a parsed version from all of the config
        files.
        """
        return self._parsed_dict

    @parsed_dict.setter
    def _set_parsed_dict(self, val: dict) -> None:
        """Updates the parsed Dict with new values.

        ..NOTE::
        Expected to be used only in tests!
        """
        self._parsed_dict.update(val)

    @abstractmethod
    def parse(self, files: list) -> None:
        """Parse files into the instances `parsed_dict`.

        :param list files: List of files to parse. Note that subsequent files
            **will** override the value of any prior duplicate keys!
        :returns: None.
        """
