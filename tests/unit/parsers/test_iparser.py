"""Tests for the implemented interface methods."""
import pytest
from src.config_file_parser.parsers.iparser import IParser


class FakeParser(IParser):
    """Test Parser class with enough to satisfy ABC."""

    def parse(self, files: list):
        return None


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
        parser._set_parsed_dict = exp
        assert parser.parsed_dict == exp

    @pytest.mark.parametrize(
        "dict_a, dict_b,exp",
        (
            ({"a": 1, "b": 1}, {"b": 2, "c": 2}, {"a": 1, "b": 2, "c": 2}),
            ({"b": 2, "c": 2}, {"a": 1, "b": 1}, {"a": 1, "b": 1, "c": 2}),
        ),
    )
    def test_parsed_dict_updates(self, dict_a, dict_b, exp):
        parser = FakeParser()
        assert parser.parsed_dict == {}
        parser._set_parsed_dict = dict_a
        assert parser.parsed_dict == dict_a
        parser._set_parsed_dict = dict_b
        assert parser.parsed_dict == exp
