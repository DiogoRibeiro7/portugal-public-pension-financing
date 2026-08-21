"""Legal-rate registry helpers."""

from __future__ import annotations

import math
from datetime import date
from typing import Any

import pandas as pd

REQUIRED_EMPLOYER_CLASSES: frozenset[str] = frozenset(
    {
        "autonomous_entities_first_covered_2007",
        "central_state_integrated_services",
        "entities_already_contributing_before_2007",
        "entities_first_covered_2009",
    }
)

ALLOWED_REGISTRY_STATUSES: frozenset[str] = frozenset(
    {
        "current_consolidated_rule",
        "verified_official_judicial_summary",
    }
)


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


def validate_legal_contribution_registry(
    path: str,
    source_registry_path: str | None = None,
) -> list[str]:
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
        source_id = _field(record, "source_id")
        if source_id not in _legal_source_ids(source_registry_path):
            errors.append(f"Unknown legal contribution source_id on row {row_number}: {source_id}")
        status = _field(record, "status")
        if status not in ALLOWED_REGISTRY_STATUSES:
            errors.append(f"Invalid legal contribution status on row {row_number}: {status}")
        if _field(record, "covered_risks") != "retirement;survivor":
            errors.append(f"Invalid covered_risks on legal contribution row {row_number}")
        if "CGA quota" not in _field(record, "contribution_base_definition"):
            errors.append(f"Legal contribution row {row_number} must define the CGA quota base")
        effective_from = _date_value(_field(record, "effective_from"))
        effective_to = _field(record, "effective_to")
        if effective_to and _date_value(effective_to) < effective_from:
            errors.append(f"Legal contribution interval ends before it starts on row {row_number}")
        errors.extend(_validate_rate_total(record, row_number, "worker"))
        errors.extend(_validate_rate_total(record, row_number, "employer"))

    employer_classes = set(registry["employer_class"].dropna().astype(str))
    for employer_class in sorted(REQUIRED_EMPLOYER_CLASSES.difference(employer_classes)):
        errors.append(f"Missing legal contribution employer class: {employer_class}")
    for employer_class in sorted(employer_classes.difference(REQUIRED_EMPLOYER_CLASSES)):
        errors.append(f"Unexpected legal contribution employer class: {employer_class}")
    for employer_class_key, group in registry.groupby("employer_class"):
        employer_class = str(employer_class_key)
        open_rows = group[group["effective_to"].isna() | (group["effective_to"].astype(str) == "")]
        if len(open_rows) != 1:
            errors.append(f"Legal contribution class {employer_class} must have one open interval")

    errors.extend(_validate_non_overlapping_intervals(registry))
    return errors


def _legal_source_ids(source_registry_path: str | None) -> set[str]:
    if source_registry_path is None:
        return {
            "DR_EA_CONSOLIDATED",
            "TC_ACORDAO_255_2020",
            "TC_ACORDAO_362_2016",
        }
    sources = pd.read_csv(source_registry_path, dtype=str)
    return set(sources["source_id"].dropna().astype(str))


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
