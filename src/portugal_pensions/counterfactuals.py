"""Counterfactual financing utilities with explicit stock-flow consistency."""

from __future__ import annotations

from collections.abc import Sequence
import math


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
    for index, (contribution, annual_return) in enumerate(zip(contributions, annual_returns, strict=True)):
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
