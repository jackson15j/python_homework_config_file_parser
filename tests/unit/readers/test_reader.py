"""Stub Reader tests."""
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


class TestDottedPathReaderInitialRequirements:
    """Dotted Path Reader tests from the initial requirements page."""

    def test_get_returns_single_value(self):
        assert (
            reader.get("database.host", PARSED_DICT)
            == PARSED_DICT["database"]["host"]
        )

    def test_get_returns_section_value(self):
        assert reader.get("cache", PARSED_DICT) == PARSED_DICT["cache"]

    def test_get_supports_escaped_period_for_keys_with_a_period(self):
        """Test to: RAISE AS A CHALLENGE TO BASE REQUIREMENTS.

        The JSON Spec supports any unicode character (apart from an unrelated
        subset) in a string. Therefore, it is legal to have a period in a
        key. Current requirements of the problem don't state this, but this
        would most like be:

        - Added as a future requirement.
        - Raised as a Customer bug.
        - Documented as a design/known issue.

        On the assumption that it would be requested, Adding a quick test to
        support the escaped version for a Full Stop (`U+002E`).
        """
        exp = 1
        _parsed_dict = {"a.b": exp}
        assert reader.get("a.b", _parsed_dict) == {}
        assert reader.get(r"a\u002eb", _parsed_dict) == exp
