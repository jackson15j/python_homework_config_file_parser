"""Tests for the `JsonParser`."""
import json
import pytest
from pathlib import Path
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

    def test_parse_missing_file_returns_empty_dict(self, tmp_path):
        exp = {}
        f = Path("/a/non-existent/path")
        parser = JsonParser()
        parser.parse([f])
        assert parser.parsed_dict == exp

    @pytest.mark.parametrize(
        "data,exp",
        (
            (None, {}),
            ("", {}),
            ({}, {}),
            ({"a": 1}, {"a": 1}),
            ({"a": [1, 2]}, {"a": [1, 2]}),
            ({"a": {"b": 2}}, {"a": {"b": 2}}),
        ),
    )
    def test_parse_single_file(self, data, exp, tmp_path):
        file_name = "file.json"
        f = tmp_path / file_name
        f.write_text(json.dumps(data))

        parser = JsonParser()
        parser.parse([f])
        assert parser.parsed_dict == exp
        assert parser.files == [f]
        assert parser.parsed_files == [f]
        assert parser.unparseable_files == []
