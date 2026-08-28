"""Command-line entry points for repository validation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .bibliography import write_bibliography
from .validation import validate_evidence_directory, validate_manifest, validate_zenodo_metadata


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description="Portuguese pension-financing research utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser(
        "validate-evidence", help="Validate required evidence registries"
    )
    validate.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    manifest = subparsers.add_parser("validate-manifest", help="Validate MANIFEST.sha256 checksums")
    manifest.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    zenodo = subparsers.add_parser("validate-zenodo", help="Validate .zenodo.json metadata")
    zenodo.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    bibliography = subparsers.add_parser(
        "build-bibliography", help="Regenerate paper/references.bib from the literature map"
    )
    bibliography.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    validate_all = subparsers.add_parser("validate-all", help="Run all repository validations")
    validate_all.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
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
    elif args.command == "validate-manifest":
        errors = validate_manifest(args.root / "MANIFEST.sha256", args.root)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            raise SystemExit(1)
        print("Manifest checksums are valid.")
    elif args.command == "validate-zenodo":
        errors = validate_zenodo_metadata(args.root / ".zenodo.json")
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            raise SystemExit(1)
        print("Zenodo metadata is valid.")
    elif args.command == "build-bibliography":
        write_bibliography(
            args.root / "evidence" / "literature_map.csv",
            args.root / "paper" / "references.bib",
        )
        print("Bibliography regenerated from the literature map.")
    elif args.command == "validate-all":
        errors = [
            *validate_evidence_directory(args.root / "evidence"),
            *validate_manifest(args.root / "MANIFEST.sha256", args.root),
            *validate_zenodo_metadata(args.root / ".zenodo.json"),
        ]
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            raise SystemExit(1)
        print("Repository validations passed.")


if __name__ == "__main__":
    main()
