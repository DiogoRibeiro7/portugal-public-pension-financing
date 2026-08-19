"""Legal-rate registry helpers."""

from __future__ import annotations

import math
from datetime import date
from typing import Any

import pandas as pd


def statutory_liability(contribution_base: float, statutory_rate: float) -> float:
    """Compute a statutory contribution liability from a validated base and rate."""
    if not isinstance(contribution_base, (int, float)):
        raise TypeError("contribution_base must be numeric")
    if not isinstance(statutory_rate, (int, float)):
        raise TypeError("statutory_rate must be numeric")
    base = float(contribution_base)
    rate = float(statutory_rate)
    if not math.isfinite(base) or base < 0.0:
        raise ValueError("contribution_base must be finite and non-negative")
    if not math.isfinite(rate) or rate < 0.0 or rate > 1.0:
        raise ValueError("statutory_rate must be finite and between 0 and 1")
    return base * rate


def validate_legal_contribution_registry(path: str) -> list[str]:
    """Return validation errors for the legal contribution registry."""
    registry = pd.read_csv(path, dtype=str)
    required_columns = {
        "effective_from",
        "effective_to",
        "employer_class",
        "worker_rate_retirement",
        "worker_rate_survivor",
        "worker_rate_total",
        "employer_rate_retirement",
        "employer_rate_survivor",
        "employer_rate_total",
        "contribution_base_definition",
        "covered_risks",
        "source_id",
        "article",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(registry.columns))
    if missing_columns:
        return [f"Legal contribution registry missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    key_columns = ["effective_from", "effective_to", "employer_class"]
    duplicates = registry[registry.duplicated(subset=key_columns, keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate legal contribution interval: "
            f"{_field(duplicate_row, 'employer_class')} {_field(duplicate_row, 'effective_from')}"
        )

    for row_number, record in enumerate(registry.to_dict("records"), start=2):
        for column in required_columns.difference({"effective_to"}):
            if not _field(record, column):
                errors.append(f"Missing {column} on legal contribution row {row_number}")
        errors.extend(_validate_rate_total(record, row_number, "worker"))
        errors.extend(_validate_rate_total(record, row_number, "employer"))

    errors.extend(_validate_non_overlapping_intervals(registry))
    return errors


def _validate_rate_total(row: Any, row_number: int, prefix: str) -> list[str]:
    retirement = _rate(row, f"{prefix}_rate_retirement")
    survivor = _rate(row, f"{prefix}_rate_survivor")
    total = _rate(row, f"{prefix}_rate_total")
    if not math.isclose(retirement + survivor, total, rel_tol=0.0, abs_tol=1e-12):
        return [f"{prefix} rate components do not sum on legal contribution row {row_number}"]
    return []


def _validate_non_overlapping_intervals(registry: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    for employer_class, group in registry.groupby("employer_class"):
        intervals = sorted(
            (
                _date_value(row["effective_from"]),
                _date_value(row["effective_to"]) if _field(row, "effective_to") else date.max,
            )
            for _, row in group.iterrows()
        )
        for (_, previous_end), (current_start, _) in zip(intervals, intervals[1:], strict=False):
            if current_start <= previous_end:
                errors.append(f"Overlapping legal contribution intervals for {employer_class}")
                break
    return errors


def _rate(row: Any, column: str) -> float:
    value = _field(row, column)
    try:
        rate = float(value)
    except ValueError as exc:
        raise ValueError(f"{column} must be numeric") from exc
    if not math.isfinite(rate) or rate < 0.0 or rate > 1.0:
        raise ValueError(f"{column} must be finite and between 0 and 1")
    return rate


def _date_value(value: Any) -> date:
    return date.fromisoformat(str(value))


def _field(row: Any, column: str) -> str:
    value = row[column]
    if pd.isna(value):
        return ""
    return str(value).strip()
