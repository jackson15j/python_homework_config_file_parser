"""Interface that all Parser's inherit."""
from logging import getLogger
from pathlib import Path

from abc import ABC, abstractmethod

log = getLogger(__name__)


class FileNotFound(Exception):
    """File not found exception."""


class ParseException(Exception):
    """Failed to parse content exception."""


class IParser(ABC):
    """Base Parser."""

    def __init__(self):
        self._files: list[Path] = []
        self._unparseable_files: list[Path] = []
        self._parsed_files: list[Path] = []
        self._parsed_dict: dict = {}

    @property
    def files(self) -> list:
        """Returns list of supplied files to parse."""
        return self._files

    @files.setter
    def files(self, filepath: list[Path]) -> None:
        """Updates the (original) Files list with the supplied file list."""
        self._files = filepath

    @property
    def unparseable_files(self) -> list:
        """Returns list of files that were **NOT** parsed."""
        return self._unparseable_files

    @unparseable_files.setter
    def unparseable_files(self, filepath: Path) -> None:
        """Updates the Unparseable Files list with the supplied file."""
        self.unparseable_files.append(filepath)

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
        if val is None:
            return
        self._parsed_dict.update(val)

    @staticmethod
    def _read_file_contents(filepath: Path) -> str:
        """Reads file contents to a string.

        :param pathlib.Path filepath: file to read.
        :returns: str.
        :raises: FileNotFound.
        """
        if not filepath.exists():
            raise FileNotFound(f"{filepath} does not exist!")
        return filepath.read_text()

    @abstractmethod
    def _parse_content(self, data: str) -> dict:
        """Parse content schema to a python dict.

        :param str data: Content to parse to a python dict.
        :returns: dict.
        :raises: ParseException.
        """

    def parse(self, files: list[Path]) -> None:
        """Parse files into the instances `parsed_dict`.

        :param list files: List of files to parse. Note that subsequent files
            **will** override the value of any prior duplicate keys!
        :returns: None.
        """
        self.files = files
        for filepath in files:
            _data = ""
            _dict = {}
            try:
                # FIXME: #6 Decouple file reading and parsing to simplify
                # testing. eg. File reading function creates a list of tuples:
                # `[(<file>, <content>), ...]`, to parse later on.
                #
                # - PRO: Decoupled code, easier to test.
                # - CON: Storing in memory, could`ve changed code to use a
                #   generator.
                _data = self._read_file_contents(filepath)
            except FileNotFound as e:
                log.warning(e)
                self.unparseable_files = filepath

            try:
                _dict = self._parse_content(_data)
            except ParseException as e:
                log.warning(e)
                self._unparseable_files.append(filepath)

            self.parsed_dict = _dict
            self.parsed_files = filepath
            log.debug("Successfully parsed config file:  %s.", filepath)
