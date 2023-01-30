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
        self._unparsed_files: list[Path] = []
        self._content_to_parse: list[tuple[Path, str]] = []
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
    def content_to_parse(self) -> list[tuple[Path, str]]:
        """Returns list of tuples of filepath + content, to be parsed."""
        return self._content_to_parse

    @content_to_parse.setter
    def content_to_parse(self, filepath_and_content: tuple) -> None:
        """Updates list of tuples of filepath + content.."""
        # TODO: #6 Move File reading to it's own class and feed this into the
        # parser at either construction time or directly into the parse
        # function.
        self.content_to_parse.append((filepath_and_content))

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

    def _read_file_contents(self, filepath: Path) -> None:
        """Reads file contents to a string.

        :param pathlib.Path filepath: file to read.
        :returns: None.
        :raises: FileNotFound.
        """
        if not filepath.exists():
            raise FileNotFound(f"{filepath} does not exist!")
        _content = filepath.read_text()
        self.content_to_parse = (filepath, _content)

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
                self._read_file_contents(filepath)
            except FileNotFound as e:
                log.warn(e)
                self.unparsed_files = filepath

            try:
                _dict = self._parse_content(_data)
            except ParseException as e:
                log.warn(e)
                self._unparsed_files.append(filepath)

            self.parsed_dict = _dict
            self.parsed_files = filepath
            log.debug("Successfully parsed config file:  %s.", filepath)
