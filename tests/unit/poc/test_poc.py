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
        ),
    )
    def test_graceful_response_from_invalid_parsed_content(
        self, data, dot_path, exp, tmp_path
    ):
        """Verify invalid file contents parses to an arbitrary empty value,
        instead of throwing an exception.

        ..NOTE::
          Separated from below identical test, to support a Production code
          change to test Parser Exceptions being reported back to the User.
        """
        f = tmp_path / "file.json"
        f.write_text(json.dumps(data))

        parser = PoC([f])
        assert parser.look_up(dot_path) == exp

    @pytest.mark.parametrize(
        "data,dot_path,exp",
        (
            ({"a": 1}, "a", 1),
            ({"a": [1, 2]}, "a", [1, 2]),
            ({"a": {"b": 2}}, "a", {"b": 2}),
            ({"a": {"b": 2}}, "a.b", 2),
        ),
    )
    def test_parse_single_file(self, data, dot_path, exp, tmp_path):
        """Verify dotted look-ups return the expected singular/section value."""
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
        """Verify that when we consolidate files, it overrides later files in
        the sequence over earlier.
        """
        f1 = tmp_path / "file1.json"
        f1.write_text(json.dumps(data1))
        f2 = tmp_path / "file2.json"
        f2.write_text(json.dumps(data2))

        parser = PoC([f1, f2])
        assert parser.look_up(dot_path) == exp

    def test_with_supplied_example_files(self, tmp_path):
        """Unit test with the filenames and contents of the fixture files
        supplied to verify the functionality of this Code Test.
        """
        f1 = tmp_path / "config.json"
        f1.write_text(
            json.dumps(
                {
                    "environment": "production",
                    "database": {
                        "host": "mysql",
                        "port": 3306,
                        "username": "divido",
                        "password": "divido",
                    },
                    "cache": {"redis": {"host": "redis", "port": 6379}},
                }
            )
        )
        f2 = tmp_path / "config.also_invalid.json"
        f2.write_text("This is not a valid JSON file either")
        f3 = tmp_path / "config.invalid.json"
        f3.write_text("This is not a valid JSON file")
        f4 = tmp_path / "config.local.json"
        f4.write_text(
            json.dumps(
                {
                    "environment": "development",
                    "database": {
                        "host": "127.0.0.1",
                        "port": 3306,
                        "username": "divido",
                        "password": "divido",
                    },
                    "cache": {"redis": {"host": "127.0.0.1", "port": 6379}},
                }
            )
        )

        # Alphabetical file name order.
        parser = PoC([f1, f2, f3, f4])
        assert parser.look_up("environment") == "development"
        assert parser.look_up("database.host") == "127.0.0.1"
        assert parser.look_up("cache") == {
            "redis": {"host": "127.0.0.1", "port": 6379}
        }

        # Reverse alphabetical file name order.
        parser2 = PoC([f4, f3, f2, f1])
        assert parser2.look_up("environment") == "production"
        assert parser2.look_up("database.host") == "mysql"
        assert parser2.look_up("cache") == {
            "redis": {"host": "redis", "port": 6379}
        }
