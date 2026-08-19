"""Banking-sector pension transfer calculations.

The module intentionally separates actuarial valuation from accounting reconciliation.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence
import math


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
