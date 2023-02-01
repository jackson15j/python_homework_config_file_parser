"""Tests for the Proof of Concept class."""
import json
import pytest
from src.config_file_parser.poc.poc import PoC


class TestPoC:
    """Tests for the Proof of Concept class."""

    @pytest.mark.parametrize(
        "data,dot_path,exp",
        (
            ("", "not.found", {}),
            ({}, "not.found", {}),
            ({"a": 1}, "a", 1),
            ({"a": [1, 2]}, "a", [1, 2]),
            ({"a": {"b": 2}}, "a", {"b": 2}),
            ({"a": {"b": 2}}, "a.b", 2),
        ),
    )
    def test_parse_single_file(self, data, dot_path, exp, tmp_path):
        f = tmp_path / "file.json"
        f.write_text(json.dumps(data))

        parser = PoC([f])
        assert parser.look_up(dot_path) == exp

    @pytest.mark.parametrize(
        "data1,data2,dot_path,exp",
        (
            ({"a": 1}, {"a": 1}, "a", 1),
            ({"a": [1, 2]}, {"a": [3, 4]}, "a", [3, 4]),
            ({"a": {"b": 2}}, {"a": {"b": 3}}, "a", {"b": 3}),
            ({"a": {"b": 2}}, {"a": {"b": 3}}, "a.b", 3),
            ({"a": {"b": 2}}, {"a": {"b": 3}}, "a.c", {}),
            ({"a": {"b": 2, "c": 2}}, {"a": {"c": 3}}, "a", {"c": 3}),
            ({"a": {"b": 2, "c": 2}}, {"a": {"c": 3}}, "a.b", {}),
            ({"a": {"b": 2, "c": 2}}, {"a": {"c": 3}}, "a.c", 3),
            (
                {"a": [{"b": 2}, {"c": 2}]},
                {"a": [{"c": 3}]},
                "a",
                [{"c": 3}],
            ),
        ),
    )
    def test_parse_multiple_files(self, data1, data2, dot_path, exp, tmp_path):
        f1 = tmp_path / "file1.json"
        f1.write_text(json.dumps(data1))
        f2 = tmp_path / "file2.json"
        f2.write_text(json.dumps(data2))

        parser = PoC([f1, f2])
        assert parser.look_up(dot_path) == exp
