"""Entry Point into the Config File Parser library."""
from pathlib import Path
from src.config_file_parser.parsers.json_parser import JsonParser
from src.config_file_parser.readers import reader
from src.config_file_parser.poc.poc import get_cli_args


def main(dotted_path: str, files: list[Path]):
    """Run the Config File Parser from the original Solution implementation."""
    parser = JsonParser()
    parser.parse(files)
    ret_val = reader.get(dotted_path, parser.parsed_dict)
    return ret_val


if __name__ == "__main__":
    args = get_cli_args().parse_args()
    main(args.dotted_path, args.files)
