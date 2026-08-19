from pathlib import Path

from portugal_pensions.accounting import reconcile_financing_identity, validate_cga_financing_ledger


def test_financing_identity_reconciles() -> None:
    result = reconcile_financing_identity(
        employee_contributions=100.0,
        employer_contributions=50.0,
        state_transfers=30.0,
        other_financing=20.0,
        pension_expenditure=180.0,
        administrative_expenditure=10.0,
        other_expenditure=0.0,
        change_in_financial_position=10.0,
        tolerance=0.0,
    )
    assert result.reconciled
    assert result.residual == 0.0


def test_financing_identity_keeps_residual_uninterpreted() -> None:
    result = reconcile_financing_identity(
        employee_contributions=100.0,
        employer_contributions=0.0,
        state_transfers=0.0,
        other_financing=0.0,
        pension_expenditure=90.0,
        administrative_expenditure=0.0,
        other_expenditure=0.0,
        change_in_financial_position=0.0,
        tolerance=1.0,
    )
    assert not result.reconciled
    assert result.residual == 10.0


def test_repository_cga_financing_ledger_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_cga_financing_ledger(str(root / "data" / "processed" / "cga_financing_ledger.csv"))
        == []
    )


def test_complete_cga_financing_ledger_requires_components(tmp_path: Path) -> None:
    ledger = tmp_path / "cga_financing_ledger.csv"
    ledger.write_text(
        "year,source_id,unit,price_basis,accounting_basis,perimeter,employee_quotations,"
        "employer_contributions,state_budget_transfers,other_public_transfers,"
        "investment_income,pension_expenditure,other_benefits,administration,"
        "contributor_count,pensioner_count,contribution_base_payroll,"
        "published_additional_state_transfer,reported_global_balance,pt_pension_fund_effect,"
        "reported_global_balance_ex_pt_fund,identity_residual,status,notes\n"
        "2011,SRC,EUR_million,current,basis,perimeter,,,,,,,,,,,,,186.2,476.7,"
        "-290.6,,complete,notes\n",
        encoding="utf-8",
    )

    errors = validate_cga_financing_ledger(str(ledger))
    assert "Complete CGA ledger row 2 missing employee_quotations" in errors
