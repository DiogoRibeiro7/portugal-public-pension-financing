from pathlib import Path

import pytest

from portugal_pensions.banking import (
    bank_transfer_balance,
    present_value,
    validate_bank_asset_liability_outputs,
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


def test_repository_bank_asset_liability_outputs_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_asset_liability_outputs(
            str(root / "data" / "processed" / "bank_asset_liability_audit.csv"),
            str(root / "data" / "processed" / "bank_asset_trace.csv"),
            str(root / "data" / "processed" / "bank_asset_liability_sensitivity.csv"),
        )
        == []
    )


def test_bank_asset_liability_sensitivity_requires_rate_surface(tmp_path: Path) -> None:
    audit = tmp_path / "audit.csv"
    trace = tmp_path / "trace.csv"
    sensitivity = tmp_path / "sensitivity.csv"
    audit.write_text(
        "audit_id,year,institution,unit,price_basis,accounting_basis,"
        "liability_pv_legal_4pct,assets_transferred_total,cash_transferred,"
        "portuguese_public_debt_transferred,other_assets_transferred,"
        "statutory_equality_residual,discount_rate_sensitivity_min,"
        "discount_rate_sensitivity_max,mortality_sensitivity_status,source_ids,status,notes\n"
        "BANK_AL_AGG_2011_OPERATION,2011,aggregate,EUR_million,current,basis,"
        "5993.2,,,,,,0.02,0.06,blocked,SRC,partial_aggregate_extract,notes\n"
        "BANK_AL_AGG_2011_STATE_RECEIPT,2011,aggregate,EUR_million,current,basis,"
        ",3263.1,,,,,0.02,0.06,blocked,SRC,partial_aggregate_extract,notes\n",
        encoding="utf-8",
    )
    trace.write_text(
        "institution,asset_type,transfer_value,destination,accounting_treatment,source_id,"
        "status,notes\n"
        "aggregate_banking_sector,asset,3263.1,State,treatment,SRC,partial_aggregate_extract,"
        "notes\n",
        encoding="utf-8",
    )
    sensitivity.write_text(
        "scenario_id,institution,discount_rate,mortality_assumption,liability_pv,"
        "delta_vs_legal_4pct,unit,source_ids,status,notes\n"
        "S1,aggregate,0.04,legal,,,EUR_million,SRC,"
        "blocked_missing_cashflow_and_demographic_inputs,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_asset_liability_outputs(str(audit), str(trace), str(sensitivity))
    assert "Bank asset-liability sensitivity must cover discount rates 0.02-0.06" in errors
