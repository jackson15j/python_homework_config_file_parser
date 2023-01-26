"""Stub Parser tests."""
from src.config_file_parser import parser

# TODO: move test data to a fixture!
PARSED_DICT = {
    "environment": "production",
    "database": {
        "host": "mysql",
        "port": 3306,
        "username": "divido",
        "password": "divido",
    },
    "cache": {"redis": {"host": "redis", "port": 6379}},
}


class TestParserInitialRequirements:
    """Parser tests from the initial requirements page."""

    def test_get_returns_single_value(self):
        assert parser.get("database.host") == PARSED_DICT["database"]["host"]

    def test_get_returns_section_value(self):
        assert parser.get("cache") == PARSED_DICT["cache"]
