"""Banking-sector pension transfer calculations.

The module intentionally separates actuarial valuation from accounting reconciliation.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True, slots=True)
class BankTransferBalance:
    """Annual cash reconciliation for transferred banking-sector pensions."""

    expenditure: float
    financing: float
    residual_burden: float


def _finite(value: float, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    return numeric


def present_value(cash_flows: Sequence[float], annual_discount_rate: float) -> float:
    """Return the end-of-period present value of deterministic annual cash flows.

    Args:
        cash_flows: Cash flows at t=1, ..., n.
        annual_discount_rate: Annual effective discount rate. Must exceed -1.

    Returns:
        Present value at t=0.
    """
    rate = _finite(annual_discount_rate, "annual_discount_rate")
    if rate <= -1.0:
        raise ValueError("annual_discount_rate must be greater than -1")
    values: list[float] = []
    for index, cash_flow in enumerate(cash_flows, start=1):
        amount = _finite(cash_flow, f"cash_flows[{index - 1}]")
        values.append(amount / ((1.0 + rate) ** index))
    return float(sum(values))


def bank_transfer_balance(
    *,
    pension_expenditure: float,
    administrative_cost: float,
    state_specific_transfer: float,
    attributable_asset_financing: float = 0.0,
    other_financing: float = 0.0,
) -> BankTransferBalance:
    """Compute the annual residual funding burden of transferred bank pensions.

    A positive residual means pension and administrative expenditure exceeds the recorded
    financing sources supplied to this ledger. It must not automatically be interpreted as
    a loss to Social Security until timing and perimeter adjustments have been investigated.
    """
    expenditure = _finite(pension_expenditure, "pension_expenditure") + _finite(
        administrative_cost, "administrative_cost"
    )
    financing = (
        _finite(state_specific_transfer, "state_specific_transfer")
        + _finite(attributable_asset_financing, "attributable_asset_financing")
        + _finite(other_financing, "other_financing")
    )
    return BankTransferBalance(
        expenditure=expenditure,
        financing=financing,
        residual_burden=expenditure - financing,
    )


def required_assets_for_cash_flows(
    cash_flows: Sequence[float], annual_discount_rate: float
) -> float:
    """Alias with domain semantics for pension-liability sensitivity analysis."""
    return present_value(cash_flows, annual_discount_rate)


def validate_bank_pension_transfer_registry(path: str) -> list[str]:
    """Return validation errors for the bank pension-transfer legal registry."""
    registry = pd.read_csv(path, dtype=str)
    required_columns = {
        "record_id",
        "legal_source_id",
        "instrument",
        "publication_date",
        "effective_date",
        "category",
        "article",
        "subject",
        "legal_rule",
        "value",
        "unit",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(registry.columns))
    if missing_columns:
        return [f"Bank pension transfer registry missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = registry[registry.duplicated(subset=["record_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate bank transfer registry record_id: {_field(duplicate_row, 'record_id')}"
        )

    required_categories = {
        "pensions_assumed",
        "liabilities_retained_by_banks",
        "assets_transferred",
        "state_financing",
        "valuation_date",
        "legal_discount_rate",
        "mortality_table",
        "independent_valuation",
        "asset_composition_constraint",
        "transfer_schedule",
        "participating_institution",
        "extinguishment_rule",
    }
    categories = set(registry["category"].dropna().astype(str))
    for category in sorted(required_categories.difference(categories)):
        errors.append(f"Missing DL127 bank transfer category: {category}")

    institution_count = int((registry["category"].astype(str) == "participating_institution").sum())
    if institution_count != 18:
        errors.append(f"Expected 18 participating institutions, found {institution_count}")

    for row_number, record in enumerate(registry.to_dict("records"), start=2):
        for column in required_columns.difference({"value", "unit"}):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank transfer registry row {row_number}")
        status = _field(record, "status")
        if status not in {"source_acquired", "official_detail_registered"}:
            errors.append(f"Unexpected bank transfer registry status on row {row_number}: {status}")

    expected_numeric = {
        "DL127_VALUATION_2": 0.04,
        "DL127_VALUATION_6": 0.005,
        "DL127_ASSET_2": 0.50,
        "DL127_SCHEDULE_1": 0.55,
        "DL127_SCHEDULE_3": 0.95,
    }
    for record_id, expected_value in expected_numeric.items():
        matches = registry[registry["record_id"] == record_id]
        if matches.empty:
            errors.append(f"Missing bank transfer numeric row: {record_id}")
            continue
        actual = _field(matches.iloc[0], "value")
        if not actual or not math.isclose(
            float(actual), expected_value, rel_tol=0.0, abs_tol=1e-12
        ):
            errors.append(f"Unexpected value for {record_id}: {actual}")
    return errors


def _field(row: Any, column: str) -> str:
    value = row[column]
    if pd.isna(value):
        return ""
    return str(value).strip()
