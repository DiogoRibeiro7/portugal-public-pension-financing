"""Command-line entry points for repository validation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .validation import validate_evidence_directory


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description="Portuguese pension-financing research utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate-evidence", help="Validate required evidence registries")
    validate.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    return parser


def main() -> None:
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "validate-evidence":
        evidence_dir = args.root / "evidence"
        errors = validate_evidence_directory(evidence_dir)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            raise SystemExit(1)
        print("Evidence registry structure is valid.")


if __name__ == "__main__":
    main()
