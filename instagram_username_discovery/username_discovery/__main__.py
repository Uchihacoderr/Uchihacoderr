"""Command-line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from .generator import two_character_count
from .ledger import export_candidates, validate_csv


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="username-discovery",
        description="Generate short Instagram username candidates and maintain a manual evidence ledger.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="generate a CSV candidate ledger")
    generate.add_argument("--length", type=int, help="generate exactly this length")
    generate.add_argument("--min-length", type=int, default=2)
    generate.add_argument("--max-length", type=int, default=2)
    generate.add_argument("--output", default="data/username_candidates.csv")

    validate = subparsers.add_parser("validate", help="validate a generated CSV")
    validate.add_argument("csv_path")

    stats = subparsers.add_parser("stats", help="show default two-character search-space size")

    args = parser.parse_args()

    if args.command == "generate":
        minimum = args.length if args.length is not None else args.min_length
        maximum = args.length if args.length is not None else args.max_length
        count = export_candidates(args.output, minimum, maximum)
        print(f"Generated {count:,} candidates: {Path(args.output).resolve()}")
        print("Availability has NOT been checked. All rows are NOT_CHECKED.")
    elif args.command == "validate":
        count, errors = validate_csv(args.csv_path)
        print(f"Rows checked: {count:,}")
        if errors:
            print("\n".join(errors))
            raise SystemExit(1)
        print("CSV structure and username syntax look valid.")
    elif args.command == "stats":
        print(f"Default two-character candidates: {two_character_count():,}")


if __name__ == "__main__":
    main()
