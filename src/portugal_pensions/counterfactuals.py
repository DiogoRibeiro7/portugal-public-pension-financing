"""Counterfactual financing utilities with explicit stock-flow consistency."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

import pandas as pd


def _finite(value: float, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def compound_reserve(
    contributions: Sequence[float],
    annual_returns: Sequence[float],
    *,
    initial_reserve: float = 0.0,
) -> list[float]:
    """Accumulate a hypothetical funded reserve.

    Contributions are assumed to enter at the start of each period and then earn that
    period's return. A funded-reserve counterfactual must be recorded as additional public
    expenditure unless another financing source is explicitly removed.
    """
    if len(contributions) != len(annual_returns):
        raise ValueError("contributions and annual_returns must have the same length")
    reserve = _finite(initial_reserve, "initial_reserve")
    path: list[float] = []
    for index, (contribution, annual_return) in enumerate(
        zip(contributions, annual_returns, strict=True)
    ):
        flow = _finite(contribution, f"contributions[{index}]")
        rate = _finite(annual_return, f"annual_returns[{index}]")
        if rate <= -1.0:
            raise ValueError("annual returns must be greater than -1")
        reserve = (reserve + flow) * (1.0 + rate)
        path.append(reserve)
    return path


def funding_substitution(
    observed_state_transfer: float,
    counterfactual_employer_contribution: float,
) -> tuple[float, float]:
    """Substitute employer financing for State transfers without creating free resources.

    Returns:
        A tuple ``(employer_contribution, adjusted_state_transfer)``.
    """
    state = _finite(observed_state_transfer, "observed_state_transfer")
    employer = _finite(counterfactual_employer_contribution, "counterfactual_employer_contribution")
    adjusted_state = max(0.0, state - employer)
    effective_employer = min(employer, state)
    return effective_employer, adjusted_state


def validate_public_worker_reallocation(
    cohort_path: str,
    contribution_path: str,
) -> list[str]:
    """Return validation errors for post-2006 public-worker reallocation files."""
    cohorts = pd.read_csv(cohort_path, dtype=str)
    contributions = pd.read_csv(contribution_path, dtype=str)
    errors = [
        *_validate_reallocation_table(
            cohorts,
            required_columns={
                "year",
                "cohort",
                "lower",
                "central",
                "upper",
                "unit",
                "source_ids",
                "status",
                "notes",
            },
            table_name="public worker cohort",
            value_columns={"lower", "central", "upper"},
            duplicate_columns=["year", "cohort"],
        ),
        *_validate_reallocation_table(
            contributions,
            required_columns={
                "year",
                "employee_contributions_lower",
                "employee_contributions_central",
                "employee_contributions_upper",
                "employer_contributions_lower",
                "employer_contributions_central",
                "employer_contributions_upper",
                "unit",
                "source_ids",
                "observation_type",
                "status",
                "notes",
            },
            table_name="public worker contribution",
            value_columns={
                "employee_contributions_lower",
                "employee_contributions_central",
                "employee_contributions_upper",
                "employer_contributions_lower",
                "employer_contributions_central",
                "employer_contributions_upper",
            },
            duplicate_columns=["year"],
        ),
    ]
    for table_name, table in (
        ("public worker cohort", cohorts),
        ("public worker contribution", contributions),
    ):
        years = sorted(int(_field(record, "year")) for record in table.to_dict("records"))
        if years != list(range(2006, 2026)):
            errors.append(f"{table_name} table must cover every year from 2006 to 2025")
    return errors


def _validate_reallocation_table(
    table: pd.DataFrame,
    *,
    required_columns: set[str],
    table_name: str,
    value_columns: set[str],
    duplicate_columns: list[str],
) -> list[str]:
    missing_columns = sorted(required_columns.difference(table.columns))
    if missing_columns:
        return [f"{table_name} table missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = table[table.duplicated(subset=duplicate_columns, keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(f"Duplicate {table_name} row for year {_field(duplicate_row, 'year')}")

    for row_number, record in enumerate(table.to_dict("records"), start=2):
        for column in required_columns.difference(value_columns):
            if not _field(record, column):
                errors.append(f"Missing {column} on {table_name} row {row_number}")
        status = _field(record, "status")
        if not (status.startswith("blocked") or status in {"estimated", "complete"}):
            errors.append(f"Unexpected {table_name} status on row {row_number}: {status}")
        for column in value_columns:
            value = _field(record, column)
            if value and _finite(float(value), column) < 0.0:
                errors.append(f"{column} must be non-negative on {table_name} row {row_number}")
    return errors


def _field(row: Any, column: str) -> str:
    value = row[column]
    if pd.isna(value):
        return ""
    return str(value).strip()
