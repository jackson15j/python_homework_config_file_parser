"""Read JSON files and gracefully parse them in order."""
import json
from src.config_file_parser.parsers.iparser import ParseException
from src.config_file_parser.parsers.iparser import IParser


class JsonParser(IParser):
    """Read JSON files and gracefully parse them in order."""

    def __init__(self):
        super().__init__()

    def _parse_content(self, data: str) -> dict:
        """Parse content schema to a python dict.

        :param str data: Content to parse to a python dict.
        :returns: dict.
        :raises: ParseException.
        """
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise ParseException("Error parsing the JSON content!") from e
