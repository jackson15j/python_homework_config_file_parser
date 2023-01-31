"""Tests for the implemented interface methods."""
from pathlib import Path
import pytest
from src.config_file_parser.parsers.iparser import FileNotFound
from src.config_file_parser.parsers.iparser import IParser


class FakeParser(IParser):
    """Test Parser class with enough to satisfy ABC.

    ..NOTE::

        In non-interface code, where I was directly using the class under test,
        I would typically test in the following ways:

        * Monkey Patch if I need to inject state into a variable/call buried
          within a function.
        * Refactor buried variable/call to be passed into the function under
          test. ie. harden contract boundaries, decouple code, remove the need
          to Monkey Patch.
    """

    _inject_parsed_dict: dict = {}

    @staticmethod
    def _read_file_contents(_):
        """Overriding this method since it will be done in an integration test
        or downstream unittests with `tmp_path`."""
        return ""

    def _parse_content(self, _):
        return self._inject_parsed_dict


class TestIParser:
    """Tests for the implemented interface methods."""

    # TODO: convert to a base test class so that I can re-use on the classes
    # that inherit from `IParser`.

    def test_get_files_initial_is_empty(self):
        assert FakeParser().files == []

    def test_get_parsed_files_initial_is_empty(self):
        assert FakeParser().parsed_files == []

    def test_get_parsed_dict_initial_is_empty(self):
        assert FakeParser().parsed_dict == {}

    def test_get_parsed_dict_after_set(self):
        exp = {"a": 1}
        parser = FakeParser()
        assert parser.parsed_dict == {}
        parser.parsed_dict = exp
        assert parser.parsed_dict == exp

    def test__read_file_contents_non_existent_file_exception(self):
        f = Path("/a/non-existent/path")
        with pytest.raises(FileNotFound, match=f"{f} does not exist!"):
            IParser._read_file_contents(f)

    def test__read_file_contents(self, tmp_path):
        exp = "file read"
        f = tmp_path / "file.txt"
        f.write_text(exp)
        assert IParser._read_file_contents(f) == exp

    @pytest.mark.parametrize(
        "dict_a, dict_b,exp",
        (
            ({"a": 1, "b": 1}, {"b": 2, "c": 2}, {"a": 1, "b": 2, "c": 2}),
            ({"b": 2, "c": 2}, {"a": 1, "b": 1}, {"a": 1, "b": 1, "c": 2}),
        ),
    )
    def test_file_parsing_to_parsed_dict_updates(
        self, dict_a, dict_b, exp, tmp_path
    ):
        """End-to-End test of `IParser.parse()`, but mocked out the file
        handling to keep it as a unit test."""
        parser = FakeParser()
        # NOT populating temp files with content, due to overriding the
        # file-handling code.
        file_a = tmp_path / "file_a"
        file_b = tmp_path / "file_b"

        assert parser.parsed_dict == {}
        # Injecting state due to overriding file reads.
        parser._inject_parsed_dict = dict_a
        parser.parse([file_a])
        assert parser.parsed_dict == dict_a
        parser._inject_parsed_dict = dict_b
        # Explicitly parse multiple _"files"_.
        parser.parse([file_b])
        assert parser.parsed_dict == exp
