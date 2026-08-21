"""Helpers for auditable source extraction records."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractionRecord:
    """Machine-readable locator for a source extraction."""

    source_id: str
    page: str
    table_title: str
    row_label: str
    column_label: str
    original_text: str
    parsed_value: str
    unit: str
    extraction_method: str
    validation_method: str
    qa_tier: str
    secondary_check: str
    parsing_warning: str
    status: str
    notes: str

    def as_csv_row(self) -> dict[str, str]:
        """Return a CSV-serializable row."""
        return {
            "source_id": self.source_id,
            "page": self.page,
            "table_title": self.table_title,
            "row_label": self.row_label,
            "column_label": self.column_label,
            "original_text": self.original_text,
            "parsed_value": self.parsed_value,
            "unit": self.unit,
            "extraction_method": self.extraction_method,
            "validation_method": self.validation_method,
            "qa_tier": self.qa_tier,
            "secondary_check": self.secondary_check,
            "parsing_warning": self.parsing_warning,
            "status": self.status,
            "notes": self.notes,
        }


def normalize_extraction_text(value: str) -> str:
    """Collapse whitespace while preserving the source string content."""
    if not isinstance(value, str):
        raise TypeError("value must be str")
    return re.sub(r"\s+", " ", value).strip()


def parse_accounting_number(value: str) -> float:
    """Parse a Portuguese/English accounting number into a float."""
    if not isinstance(value, str):
        raise TypeError("value must be str")
    text = normalize_extraction_text(value)
    if not text:
        raise ValueError("value is empty")

    negative = text.startswith("(") and text.endswith(")")
    cleaned = text.strip("()").replace("%", "").replace("€", "")
    cleaned = cleaned.replace("EUR", "").replace("MEUR", "").strip()
    cleaned = cleaned.replace(" ", "")

    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")

    match = re.search(r"[-+]?\d+(?:\.\d+)?", cleaned)
    if match is None:
        raise ValueError(f"no numeric value found: {value}")
    parsed = float(match.group(0))
    return -parsed if negative else parsed
