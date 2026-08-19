import pytest

from portugal_pensions.legal import statutory_liability


def test_statutory_liability() -> None:
    assert statutory_liability(1_000.0, 0.10) == pytest.approx(100.0)


def test_rate_must_be_fraction() -> None:
    with pytest.raises(ValueError):
        statutory_liability(1_000.0, 1.1)
