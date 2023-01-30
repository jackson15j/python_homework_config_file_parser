"""Interface that all Parser's inherit."""
from pathlib import Path

from abc import ABC, abstractmethod



class FileNotFound(Exception):
    """File not found exception."""


class ParseException(Exception):
    """Failed to parse content exception."""


class IParser(ABC):
    """Base Parser."""

    def __init__(self):
        self._files: list[Path] = []
        self._unparsed_files: list[Path] = []
        self._parsed_files: list[Path] = []
        self._parsed_dict: dict = {}

    @property
    def files(self) -> list:
        """Returns list of supplied files to parse."""
        return self._files

    @property
    def unparsed_files(self) -> list:
        """Returns list of files that were **NOT** parsed."""
        return self._unparsed_files

    @unparsed_files.setter
    def unparsed_files(self, filepath: Path) -> None:
        """Updates the Unparsed Files list with the supplied file."""
        self.unparsed_files.append(filepath)

    @property
    def parsed_files(self) -> list:
        """Returns list of files that were parsed."""
        return self._parsed_files

    @parsed_files.setter
    def parsed_files(self, filepath: Path) -> None:
        """Updates the Parsed Files list with the supplied parsed file."""
        self.parsed_files.append(filepath)

    @property
    def parsed_dict(self) -> dict:
        """Returns Dict containing a parsed version from all of the config
        files.
        """
        return self._parsed_dict

    @parsed_dict.setter
    def parsed_dict(self, val: dict) -> None:
        """Updates the parsed Dict with new values.

        ..NOTE::
            Expected to be used only in tests!
        """
        self._parsed_dict.update(val)

    @abstractmethod
    def parse(self, files: list[Path]) -> None:
        """Parse files into the instances `parsed_dict`.

        :param list files: List of files to parse. Note that subsequent files
            **will** override the value of any prior duplicate keys!
        :returns: None.
        """
