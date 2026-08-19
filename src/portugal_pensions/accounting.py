"""Transparent accounting identities used by the research notebooks."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True, slots=True)
class FinancingIdentityResult:
    """Result of an annual financing reconciliation.

    Attributes:
        total_financing: Sum of contribution, transfer and other financing inflows.
        total_use: Sum of benefit, administrative and other expenditure outflows.
        residual: Financing minus uses minus the reported change in financial position.
        reconciled: Whether the absolute residual is within the supplied tolerance.
    """

    total_financing: float
    total_use: float
    residual: float
    reconciled: bool


def _finite_nonnegative(value: float, name: str) -> float:
    """Validate a non-negative finite monetary input."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    if numeric < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return numeric


def reconcile_financing_identity(
    *,
    employee_contributions: float,
    employer_contributions: float,
    state_transfers: float,
    other_financing: float,
    pension_expenditure: float,
    administrative_expenditure: float,
    other_expenditure: float,
    change_in_financial_position: float,
    tolerance: float = 1.0,
) -> FinancingIdentityResult:
    """Reconcile a transparent annual pension-financing identity.

    The identity is::

        financing = expenditure + change_in_financial_position + residual

    A positive residual means recorded financing exceeds recorded uses plus the reported
    change in financial position. The function does not attach an economic interpretation
    to the residual; classification and timing differences must be investigated separately.
    """
    inflows = (
        _finite_nonnegative(employee_contributions, "employee_contributions"),
        _finite_nonnegative(employer_contributions, "employer_contributions"),
        _finite_nonnegative(state_transfers, "state_transfers"),
        _finite_nonnegative(other_financing, "other_financing"),
    )
    outflows = (
        _finite_nonnegative(pension_expenditure, "pension_expenditure"),
        _finite_nonnegative(administrative_expenditure, "administrative_expenditure"),
        _finite_nonnegative(other_expenditure, "other_expenditure"),
    )
    if not isinstance(change_in_financial_position, (int, float)):
        raise TypeError("change_in_financial_position must be numeric")
    change = float(change_in_financial_position)
    if not math.isfinite(change):
        raise ValueError("change_in_financial_position must be finite")
    tol = _finite_nonnegative(tolerance, "tolerance")

    total_financing = sum(inflows)
    total_use = sum(outflows)
    residual = total_financing - total_use - change
    return FinancingIdentityResult(
        total_financing=total_financing,
        total_use=total_use,
        residual=residual,
        reconciled=abs(residual) <= tol,
    )


def validate_cga_financing_ledger(path: str) -> list[str]:
    """Return validation errors for the processed CGA financing ledger."""
    ledger = pd.read_csv(path, dtype=str)
    required_columns = {
        "year",
        "source_id",
        "unit",
        "price_basis",
        "accounting_basis",
        "perimeter",
        "employee_quotations",
        "employer_contributions",
        "state_budget_transfers",
        "other_public_transfers",
        "investment_income",
        "pension_expenditure",
        "other_benefits",
        "administration",
        "contributor_count",
        "pensioner_count",
        "contribution_base_payroll",
        "published_additional_state_transfer",
        "reported_global_balance",
        "pt_pension_fund_effect",
        "reported_global_balance_ex_pt_fund",
        "identity_residual",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(ledger.columns))
    if missing_columns:
        return [f"CGA financing ledger missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = ledger[ledger.duplicated(subset=["year", "source_id", "perimeter"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate CGA financing ledger row: "
            f"{_field(duplicate_row, 'year')} {_field(duplicate_row, 'perimeter')}"
        )

    complete_components = {
        "employee_quotations",
        "employer_contributions",
        "state_budget_transfers",
        "other_public_transfers",
        "investment_income",
        "pension_expenditure",
        "other_benefits",
        "administration",
        "identity_residual",
    }
    optional_numeric = {
        "contributor_count",
        "pensioner_count",
        "contribution_base_payroll",
        "published_additional_state_transfer",
        "reported_global_balance",
        "pt_pension_fund_effect",
        "reported_global_balance_ex_pt_fund",
    }
    for row_number, record in enumerate(ledger.to_dict("records"), start=2):
        for column in required_columns.difference({"identity_residual"}):
            if column in complete_components or column in optional_numeric:
                continue
            if not _field(record, column):
                errors.append(f"Missing {column} on CGA financing ledger row {row_number}")
        status = _field(record, "status")
        if status == "complete":
            for column in complete_components:
                if not _field(record, column):
                    errors.append(f"Complete CGA ledger row {row_number} missing {column}")
        elif not status.startswith("partial"):
            errors.append(f"Unexpected CGA financing ledger status on row {row_number}: {status}")

        for column in complete_components.union(optional_numeric):
            value = _field(record, column)
            if value:
                _numeric(value, column)
    return errors


def _numeric(value: str, name: str) -> float:
    try:
        numeric = float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    return numeric


def _field(row: Any, column: str) -> str:
    value = row[column]
    if pd.isna(value):
        return ""
    return str(value).strip()
