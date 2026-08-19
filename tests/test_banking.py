import pytest

from portugal_pensions.banking import bank_transfer_balance, present_value


def test_present_value_uses_end_of_period_cash_flows() -> None:
    result = present_value([104.0], 0.04)
    assert result == pytest.approx(100.0)


def test_bank_transfer_balance_detects_unfinanced_residual() -> None:
    result = bank_transfer_balance(
        pension_expenditure=500.0,
        administrative_cost=5.0,
        state_specific_transfer=480.0,
        attributable_asset_financing=20.0,
    )
    assert result.residual_burden == pytest.approx(5.0)


def test_discount_rate_rejects_invalid_value() -> None:
    with pytest.raises(ValueError):
        present_value([1.0], -1.0)
