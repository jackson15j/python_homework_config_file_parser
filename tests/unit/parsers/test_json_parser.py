"""Tests for the `JsonParser`."""
import json
import pytest
from src.config_file_parser.parsers.iparser import ParseException
from src.config_file_parser.parsers.json_parser import JsonParser


class TestJsonParser:
    """Tests for the `JsonParser` overridden methods and implementation."""

    def test__parse_content(self):
        exp = {"a": 1}
        assert JsonParser()._parse_content(json.dumps(exp)) == exp

    def test__parse_content_bad_json_raises(self):
        with pytest.raises(
            ParseException, match="Error parsing the JSON content!"
        ):
            JsonParser()._parse_content("Not JSON = Raise Exception!")
