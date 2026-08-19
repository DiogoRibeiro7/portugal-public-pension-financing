"""Transparent accounting identities used by the research notebooks."""

from __future__ import annotations

import math
from dataclasses import dataclass


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
