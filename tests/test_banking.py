from pathlib import Path

import pytest

from portugal_pensions.banking import (
    bank_transfer_balance,
    present_value,
    validate_bank_pension_transfer_registry,
)


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


def test_repository_bank_transfer_registry_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_pension_transfer_registry(
            str(root / "evidence" / "bank_pension_transfer_registry.csv")
        )
        == []
    )


def test_bank_transfer_registry_requires_institution_count(tmp_path: Path) -> None:
    registry = tmp_path / "bank_pension_transfer_registry.csv"
    registry.write_text(
        "record_id,legal_source_id,instrument,publication_date,effective_date,category,"
        "article,subject,legal_rule,value,unit,status,notes\n"
        "DL127_VALUATION_2,DR_DL127_2011,DL127,2011-12-31,2011-12-31,"
        "legal_discount_rate,Artigo 6,discount,rule,0.04,rate,official_detail_registered,"
        "notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_pension_transfer_registry(str(registry))
    assert "Expected 18 participating institutions, found 0" in errors
