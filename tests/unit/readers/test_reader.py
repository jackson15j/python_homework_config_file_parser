"""Stub Reader tests."""
import pytest
from src.config_file_parser.readers import reader

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


@pytest.mark.skip(
    "TODO: implement actual code, after moving to a `Lookup` module."
)
class TestDottedPathReaderInitialRequirements:
    """Dotted Path Reader tests from the initial requirements page."""

    def test_get_returns_single_value(self):
        assert reader.get("database.host") == PARSED_DICT["database"]["host"]

    def test_get_returns_section_value(self):
        assert reader.get("cache") == PARSED_DICT["cache"]
