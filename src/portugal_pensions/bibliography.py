"""Deterministic BibTeX generation from the registered literature map.

The manuscript bibliography is a derived artifact. It is generated from
``evidence/literature_map.csv`` so that a citation cannot drift away from the
registered literature record, and so that no reference can appear in the paper
without a registry row behind it.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_LITERATURE_COLUMNS: tuple[str, ...] = (
    "reference_id",
    "title",
    "year",
    "authors",
    "venue",
    "source_category",
    "source_url",
)

ENTRY_TYPES: dict[str, str] = {
    "academic_literature": "article",
    "institutional_review": "techreport",
    "technical_accounting_source": "techreport",
}

DEFAULT_ENTRY_TYPE = "misc"

UNKNOWN_YEAR_MARKER = "n.d."

_ESCAPES: tuple[tuple[str, str], ...] = (
    ("&", r"\&"),
    ("%", r"\%"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("$", r"\$"),
)


def escape_bibtex(value: str) -> str:
    """Escape the LaTeX special characters that appear in registry text."""
    if not isinstance(value, str):
        raise TypeError("value must be str")
    escaped = value
    for character, replacement in _ESCAPES:
        escaped = escaped.replace(character, replacement)
    return escaped


def cite_key(reference_id: str) -> str:
    """Return the deterministic citation key for a literature reference id."""
    if not isinstance(reference_id, str):
        raise TypeError("reference_id must be str")
    key = reference_id.strip()
    if not key:
        raise ValueError("reference_id must not be empty")
    if key.startswith("LIT_"):
        key = key[len("LIT_") :]
    return key.lower()


def _field(record: Mapping[object, Any], column: str) -> str:
    value: Any = record.get(column)
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def build_bibliography(literature_map_path: Path) -> str:
    """Render the literature map as a BibTeX database."""
    if not isinstance(literature_map_path, Path):
        raise TypeError("literature_map_path must be pathlib.Path")
    if not literature_map_path.is_file():
        raise FileNotFoundError(f"Missing literature map: {literature_map_path}")

    literature = pd.read_csv(literature_map_path, dtype=str)
    missing_columns = sorted(set(REQUIRED_LITERATURE_COLUMNS).difference(literature.columns))
    if missing_columns:
        raise ValueError(f"Literature map missing columns: {', '.join(missing_columns)}")

    header = (
        "% Generated from evidence/literature_map.csv by\n"
        "% portugal_pensions.bibliography.write_bibliography.\n"
        "% Do not edit by hand: regenerate with"
        " `python -m portugal_pensions.cli build-bibliography`.\n"
    )
    entries: list[str] = []
    for record in literature.to_dict("records"):
        reference_id = _field(record, "reference_id")
        if not reference_id:
            continue
        source_category = _field(record, "source_category")
        entry_type = ENTRY_TYPES.get(source_category, DEFAULT_ENTRY_TYPE)
        year = _field(record, "year") or UNKNOWN_YEAR_MARKER
        if year.lower() == "unknown":
            year = UNKNOWN_YEAR_MARKER
        venue_field = "journal" if entry_type == "article" else "institution"
        fields: list[tuple[str, str]] = [
            ("author", _field(record, "authors")),
            ("title", "{" + escape_bibtex(_field(record, "title")) + "}"),
            ("year", year),
            (venue_field, escape_bibtex(_field(record, "venue"))),
            ("url", _field(record, "source_url")),
        ]
        rendered = [
            f"  {name:<12}= {{{value}}}," for name, value in fields if value not in ("", "{}")
        ]
        body = "\n".join(rendered)
        entries.append(f"@{entry_type}{{{cite_key(reference_id)},\n{body}\n}}")

    return header + "\n" + "\n\n".join(entries) + "\n"


def write_bibliography(literature_map_path: Path, output_path: Path) -> None:
    """Write the generated BibTeX database to ``output_path``."""
    if not isinstance(output_path, Path):
        raise TypeError("output_path must be pathlib.Path")
    output_path.write_text(build_bibliography(literature_map_path), encoding="utf-8", newline="\n")


def validate_bibliography(bibliography_path: Path, literature_map_path: Path) -> list[str]:
    """Return validation errors for the generated manuscript bibliography."""
    for name, path in (
        ("bibliography_path", bibliography_path),
        ("literature_map_path", literature_map_path),
    ):
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")
    if not bibliography_path.is_file():
        return [f"Missing generated bibliography: {bibliography_path.name}"]
    if not literature_map_path.is_file():
        return [f"Missing literature map: {literature_map_path.name}"]

    expected = build_bibliography(literature_map_path)
    actual = bibliography_path.read_text(encoding="utf-8")
    if expected != actual:
        return [
            "Generated bibliography is stale: regenerate with "
            "`python -m portugal_pensions.cli build-bibliography`"
        ]
    return []


def validate_manuscript_citations(manuscript_path: Path, bibliography_path: Path) -> list[str]:
    """Return errors for manuscript citations that have no bibliography entry."""
    for name, path in (
        ("manuscript_path", manuscript_path),
        ("bibliography_path", bibliography_path),
    ):
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")
    if not manuscript_path.is_file() or not bibliography_path.is_file():
        return []

    text = manuscript_path.read_text(encoding="utf-8")
    bibliography = bibliography_path.read_text(encoding="utf-8")
    available = set(re.findall(r"@[a-z]+\{([^,]+),", bibliography))
    cited: set[str] = set()
    for group in re.findall(r"\\cite[tp]?\{([^}]*)\}", text):
        cited.update(key.strip() for key in group.split(",") if key.strip())
    return [
        f"Manuscript cites unknown bibliography key: {key}" for key in sorted(cited - available)
    ]
