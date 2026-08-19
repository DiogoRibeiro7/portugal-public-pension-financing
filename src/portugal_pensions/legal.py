"""Legal-rate registry helpers."""

from __future__ import annotations

import math


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
