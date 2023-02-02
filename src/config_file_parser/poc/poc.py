"""Proof of Concept to quickly parse a set of JSON files gracefully and allow a
dotted-path lookup of the consolidated structure."""
import json
from argparse import ArgumentParser
from pathlib import Path
from typing import Any


class PoC:
    """Batch read, convert, parse files to a common format and then do a
    lookup. All in a single-pass.
    """

    def __init__(self, files: list[Path]):
        _contents = self.read_files(files)
        _parsed_contents = self.parse_data_to_common_format(_contents)
        self.parsed_dict = self.consolidate(_parsed_contents)

    def read_files(self, files: list[Path]) -> list[str]:
        """Batch read into memory."""
        _contents: list[str] = []
        for filepath in files:
            if not filepath.exists():
                continue
            _contents.append(filepath.read_text())
        return _contents

    def parse_data_to_common_format(self, datas: list[str]) -> list[dict]:
        """Interchangeable Parser based on file format (eg. JSON/YAML)."""
        _contents = []
        for data in datas:
            try:
                _contents.append(json.loads(data))
            except json.JSONDecodeError:
                continue
        return _contents

    def consolidate(self, datas: list[dict]) -> dict:
        """Sequentially apply/update each common content."""
        _parsed_dict = {}
        [_parsed_dict.update(x) for x in datas]
        return _parsed_dict

    def look_up(self, dotted_path: str) -> Any:
        """Translate `dotted_path` and do a lookup on `data`."""
        # Translate dotted_path to do a dict lookup.
        _keys = dotted_path.split(".")
        cmd_str = "self.parsed_dict"
        for _key in _keys:
            # FIXME: #3 REQUIREMENTS QUERY, what should be returned on a miss?
            # `None`/`{}`, since these could be expected as data. Would usually
            # just throw an exception but the precedent in other areas is to
            # gracefully handle exceptions.
            cmd_str += f".get('{_key}', {{}})"

        # FIXME: #3 Remove this dirty, high-risk implementation with
        # `eval()`. I'm trying it for a quick way to convert a dotted-path to a
        # dictionary lookup, but it can lead to potential abuse from
        # un-validated, malformed strings passed in by the User.
        ret_val = eval(cmd_str)
        return ret_val


def get_cli_args() -> ArgumentParser:
    """Return a CLI args parser instance for downstream EntryPoint code to call
    `parse_args() on.
    """
    cli_parser = ArgumentParser(
        prog="ConfigFileParser",
        description=(
            "Read/Parse/Consolidate multiple JSON files and then allow "
            "looking up values via a dotted notation."
        ),
    )
    cli_parser.add_argument(
        "dotted_path",
        type=str,
        help=(
            "Dotted notation to do look-ups in the files provided. eg. "
            "`KeyX.SubKeyY.SubSubKeyZ`."
        ),
    )
    cli_parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help=(
            "Space separated list of 1+ files to Consolidate together (in listed "
            "order) to do a look-up from. NOTE: Latter files will override "
            "earlier files during consolidation. NOTE: Consolidation is handled "
            "in memory - Files are only read by the Application!"
        ),
    )
    return cli_parser


def get() -> Any:
    """Function to call the PoC class + lookup from a Python package
    entry-point. See: https://peps.python.org/pep-0621/#entry-points.
    """
    args = get_cli_args().parse_args()

    parser = PoC(args.files)
    return parser.look_up(args.dotted_path)
