"""CLI entry point for medconverter."""

import argparse
import signal
from pathlib import Path

from medconverter.engine import Fmt, convert
from medconverter.gui import supported_input_formats, supported_output_formats
from medconverter.utilities import create_test_json_file


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    metaparser = argparse.ArgumentParser(add_help=False)
    metaparser.add_argument("-v", "--verbose", action="store_true", help="print more informations")

    mainparser = argparse.ArgumentParser(
        description="Convert mesh files between MED and other FEA formats",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers = mainparser.add_subparsers(help="medconverter functions", dest="command")
    subparsers.add_parser("gui", help="open the GUI", parents=[metaparser])
    parser_run = subparsers.add_parser(
        "run",
        help="execute the conversion",
        description="file format is derived from file extension",
        parents=[metaparser],
    )
    parser_json = subparsers.add_parser(
        "json", help="create JSON file for test", description="input mesh in MED format"
    )

    parser_run.add_argument("input", help="input mesh path")
    parser_run.add_argument("output", help="output mesh path")
    parser_run.add_argument(
        "--input-format",
        dest="finput",
        help="input mesh format",
        choices=[Fmt.name(i) for i in supported_input_formats()],
    )
    parser_run.add_argument(
        "--output-format",
        dest="foutput",
        help="output mesh format",
        choices=[Fmt.name(i) for i in supported_output_formats()],
    )
    parser_run.add_argument(
        "--skip-types",
        nargs="*",
        type=str,
        dest="skip_types",
        help="list of cell types (origin format) to skip",
        default=[],
    )
    parser_run.add_argument(
        "--output-command",
        dest="output_comm",
        help="output command file path <code_aster>",
        default="",
    )

    parser_json.add_argument("meshpath", help="input mesh path")
    parser_json.add_argument("jsonpath", help="output json path")
    parser_json.add_argument(
        "--dir",
        action="store_true",
        dest="usedir",
        help="given paths are directories (loop over input dir items)",
    )

    args = mainparser.parse_args()

    if args.command == "gui":
        from medconverter.gui.gui import start

        start(verbose=args.verbose)

    elif args.command == "json":
        meshpath = Path(args.meshpath)
        jsonpath = Path(args.jsonpath)
        if args.usedir:
            jsonpath.mkdir(parents=True, exist_ok=True)
            for item in meshpath.iterdir():
                create_test_json_file(str(item), str(jsonpath / f"{item.stem}.json"))
        else:
            create_test_json_file(args.meshpath, args.jsonpath)

    elif args.command == "run":
        input_path = Path(args.input)
        output_path = Path(args.output)

        auto_iformat = args.finput or Fmt.name_from_extension(input_path.suffix)
        if auto_iformat == "Unknown":
            parser_run.error("Cannot derive the input format: use '--input-format'")
        auto_oformat = args.foutput or Fmt.name_from_extension(output_path.suffix)
        if auto_oformat == "Unknown":
            parser_run.error("Cannot derive the output format: use '--output-format'")

        convert(
            str(input_path),
            Fmt.get(auto_iformat),
            str(output_path),
            Fmt.get(auto_oformat),
            args.output_comm,
            args.skip_types,
            verbose=args.verbose,
        )

    else:
        mainparser.print_help()
