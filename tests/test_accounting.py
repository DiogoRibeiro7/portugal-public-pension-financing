from pathlib import Path

from portugal_pensions.accounting import (
    employee_remittance_gap,
    reconcile_financing_identity,
    validate_cga_closed_scheme_decomposition,
    validate_cga_financing_ledger,
    validate_employee_remittance_audit,
    validate_employer_contribution_audit,
    validate_pension_flow_of_funds,
    validate_state_financing_rule_registry,
)


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


def test_employee_remittance_gap_applies_explicit_adjustments() -> None:
    assert (
        employee_remittance_gap(
            withheld_from_payroll=100.0,
            recorded_cga_worker_revenue=95.0,
            timing_adjustments=-2.0,
            arrears_corrections=1.0,
            base_definition_adjustment=0.5,
            perimeter_adjustment=0.0,
        )
        == 4.5
    )


def test_repository_cga_financing_ledger_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_cga_financing_ledger(
            str(root / "data" / "processed" / "cga_financing_ledger.csv"),
            str(root / "evidence" / "source_registry.csv"),
        )
        == []
    )


def test_repository_cga_financing_ledger_covers_study_years() -> None:
    root = Path(__file__).resolve().parents[1]
    years = {
        int(row.split(",", maxsplit=1)[0])
        for row in (root / "data" / "processed" / "cga_financing_ledger.csv")
        .read_text(encoding="utf-8-sig")
        .splitlines()[1:]
    }

    assert years == set(range(1977, 2026))


def test_repository_cga_closed_scheme_decomposition_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_cga_closed_scheme_decomposition(
            str(root / "data" / "processed" / "cga_closed_scheme_decomposition.csv")
        )
        == []
    )


def test_cga_closed_scheme_blocks_incomplete_causality(tmp_path: Path) -> None:
    ledger = tmp_path / "cga_closed_scheme_decomposition.csv"
    ledger.write_text(
        "record_id,year,driver,identity_role,observed_value,counterfactual_value,"
        "balance_effect_value,unit,price_basis,accounting_basis,perimeter,source_ids,"
        "status,blocking_issue,causal_claim_permitted,notes\n"
        "ROW,2006-2025,contributor_count,driver,,,,count,not_applicable,basis,"
        "perimeter,SRC,blocked_missing_inputs,missing_counts,yes,notes\n",
        encoding="utf-8",
    )

    errors = validate_cga_closed_scheme_decomposition(str(ledger))
    assert "Incomplete CGA closed-scheme row ROW cannot permit causality" in errors


def test_repository_pension_flow_of_funds_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_pension_flow_of_funds(
            str(root / "data" / "processed" / "pension_flow_of_funds_long.csv")
        )
        == []
    )


def test_pension_flow_of_funds_rejects_duplicate_bridge_components(tmp_path: Path) -> None:
    matrix = tmp_path / "pension_flow_of_funds_long.csv"
    matrix.write_text(
        "record_id,year,transaction_id,from_entity,to_entity,flow_type,stock_flow,value,"
        "unit,price_basis,accounting_basis,source_ids,consolidation_scope,"
        "consolidates_in_general_government,bridge_definition_id,bridge_component,"
        "bridge_sign,status,notes\n"
        "R1,2011,T1,cga,consolidated_general_government,institutional_balance,balance,"
        "186.2,EUR_million,current_prices,basis,SRC,scope,not_applicable,"
        "cga_2011_balance_decomposition,reported_global_balance,1,"
        "official_account_extract,notes\n"
        "R2,2011,T2,private_pension_funds,cga,pension_fund_effect,flow,476.7,"
        "EUR_million,current_prices,basis,SRC,scope,no,cga_2011_balance_decomposition,"
        "pt_pension_fund_effect,1,official_account_extract,notes\n"
        "R3,2011,T3,cga,consolidated_general_government,institutional_balance,balance,"
        "-290.6,EUR_million,current_prices,basis,SRC,scope,not_applicable,"
        "cga_2011_balance_decomposition,reported_global_balance_ex_pt_fund,1,"
        "official_account_extract,notes\n"
        "R4,2012,T4,state_budget_treasury,social_security,state_current_transfer_financing,"
        "flow,516.0,EUR_million,current_prices,basis,SRC,scope,yes,"
        "bank_2012_cash_identity,state_current_transfer_financing,1,"
        "official_account_extract,notes\n"
        "R5,2012,T5,social_security,households_workers,pension_payment_current_expenditure,"
        "flow,516.0,EUR_million,current_prices,basis,SRC,scope,no,"
        "bank_2012_cash_identity,pension_payment_current_expenditure,-1,"
        "official_account_extract,notes\n"
        "R6,2012,T6,state_budget_treasury,social_security,oe_financing_component,"
        "flow,515.8,EUR_million,current_prices,basis,SRC,scope,yes,"
        "bank_2012_financing_split,oe_financing_component,1,"
        "official_account_extract,notes\n"
        "R7,2012,T7,cga,social_security,cga_bpn_financing_component,flow,0.1359,"
        "EUR_million,current_prices,basis,SRC,scope,yes,bank_2012_financing_split,"
        "cga_bpn_financing_component,1,official_account_extract,notes\n"
        "R8,2012,T8,private_pension_funds,state_budget_treasury,total_asset_transfer,"
        "flow,5993.2,EUR_million,current_prices,basis,SRC,scope,no,"
        "bank_2011_total_transfer_value,total_transfer_value,1,"
        "official_account_extract,notes\n"
        "R9,2012,T9,private_pension_funds,private_banks,sams_assets_returned_to_entities,"
        "flow,7.3,EUR_million,current_prices,basis,SRC,scope,no,not_applicable,"
        "not_applicable,,official_account_extract,notes\n"
        "R10,2012,T10,public_employers,cga,employer_contribution,flow,,EUR_million,"
        "current_prices,basis,SRC,scope,yes,not_applicable,not_applicable,,"
        "blocked_missing_component_values,notes\n"
        "R11,2025,T11,social_security,fefss,reserve_transfer_or_return,flow,,"
        "EUR_million,current_prices,basis,,scope,yes,not_applicable,not_applicable,,"
        "blocked_missing_component_values,notes\n"
        "R12,2011,T12,cga,consolidated_general_government,institutional_balance,"
        "balance,1.0,EUR_million,current_prices,basis,SRC,scope,not_applicable,"
        "cga_2011_balance_decomposition,reported_global_balance,1,"
        "official_account_extract,duplicate\n",
        encoding="utf-8",
    )

    assert (
        "Duplicate pension flow bridge component: "
        "cga_2011_balance_decomposition reported_global_balance"
        in validate_pension_flow_of_funds(str(matrix))
    )


def test_complete_cga_financing_ledger_requires_components(tmp_path: Path) -> None:
    ledger = tmp_path / "cga_financing_ledger.csv"
    ledger.write_text(
        "year,source_id,unit,price_basis,accounting_basis,perimeter,employee_quotations,"
        "employer_contributions,state_budget_transfers,other_public_transfers,"
        "investment_income,pension_expenditure,other_benefits,administration,"
        "contributor_count,pensioner_count,contribution_base_payroll,"
        "published_additional_state_transfer,reported_global_balance,pt_pension_fund_effect,"
        "reported_global_balance_ex_pt_fund,identity_residual,full_identity_status,"
        "balance_decomposition_residual,missing_components,status,notes\n"
        "2011,SRC,EUR_million,current,basis,perimeter,,,,,,,,,,,,,186.2,476.7,"
        "-290.6,,blocked_missing_components,0.1,,complete,notes\n",
        encoding="utf-8",
    )

    errors = validate_cga_financing_ledger(str(ledger))
    assert "Complete CGA ledger row 2 missing employee_quotations" in errors


def test_cga_financing_ledger_checks_balance_decomposition_residual(tmp_path: Path) -> None:
    ledger = tmp_path / "cga_financing_ledger.csv"
    ledger.write_text(
        "year,source_id,unit,price_basis,accounting_basis,perimeter,employee_quotations,"
        "employer_contributions,state_budget_transfers,other_public_transfers,"
        "investment_income,pension_expenditure,other_benefits,administration,"
        "contributor_count,pensioner_count,contribution_base_payroll,"
        "published_additional_state_transfer,reported_global_balance,pt_pension_fund_effect,"
        "reported_global_balance_ex_pt_fund,identity_residual,full_identity_status,"
        "balance_decomposition_residual,missing_components,status,notes\n"
        "2011,SRC,EUR_million,current,basis,perimeter,,,,,,,,,,,,,186.2,476.7,"
        "-290.6,,blocked_missing_components,9.9,employee_quotations;"
        "employer_contributions;state_budget_transfers;other_public_transfers;"
        "investment_income;pension_expenditure;other_benefits;administration;"
        "contributor_count;pensioner_count;contribution_base_payroll,"
        "partial_cge_extract,notes\n",
        encoding="utf-8",
    )

    errors = validate_cga_financing_ledger(str(ledger))
    assert "CGA balance decomposition residual fails on row 2" in errors


def test_repository_employee_remittance_audit_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_employee_remittance_audit(
            str(root / "data" / "processed" / "employee_remittance_audit.csv"),
            str(root / "evidence" / "source_registry.csv"),
        )
        == []
    )


def test_repository_employee_remittance_audit_covers_study_years() -> None:
    root = Path(__file__).resolve().parents[1]
    years = {
        int(row.split(",", maxsplit=1)[0])
        for row in (root / "data" / "processed" / "employee_remittance_audit.csv")
        .read_text(encoding="utf-8-sig")
        .splitlines()[1:]
    }

    assert years == set(range(1977, 2026))


def test_complete_employee_remittance_audit_requires_quantities(tmp_path: Path) -> None:
    audit = tmp_path / "employee_remittance_audit.csv"
    audit.write_text(
        "year,perimeter,unit,price_basis,accounting_basis,legal_worker_rate_total,"
        "legal_worker_liability,withheld_from_payroll,recorded_cga_worker_revenue,"
        "timing_adjustments,arrears_corrections,base_definition_adjustment,"
        "perimeter_adjustment,unexplained_remittance_gap,source_ids,legal_rate_basis,"
        "missing_inputs,claim_permitted,status,notes\n"
        "2011,perimeter,EUR_million,current,basis,0.11,,,,,,,,,SRC,"
        "bounded_legal_registry_worker_total,,yes,complete,notes\n",
        encoding="utf-8",
    )

    errors = validate_employee_remittance_audit(str(audit))
    assert "Complete employee remittance row 2 missing withheld_from_payroll" in errors


def test_complete_employee_remittance_audit_checks_gap_residual(tmp_path: Path) -> None:
    audit = tmp_path / "employee_remittance_audit.csv"
    audit.write_text(
        "year,perimeter,unit,price_basis,accounting_basis,legal_worker_rate_total,"
        "legal_worker_liability,withheld_from_payroll,recorded_cga_worker_revenue,"
        "timing_adjustments,arrears_corrections,base_definition_adjustment,"
        "perimeter_adjustment,unexplained_remittance_gap,source_ids,legal_rate_basis,"
        "missing_inputs,claim_permitted,status,notes\n"
        "2011,perimeter,EUR_million,current,basis,0.11,110.0,100.0,95.0,"
        "0.0,0.0,0.0,0.0,9.0,SRC,bounded_legal_registry_worker_total,,yes,"
        "complete,notes\n",
        encoding="utf-8",
    )

    errors = validate_employee_remittance_audit(str(audit))
    assert "Employee remittance gap residual fails on row 2" in errors


def test_repository_employer_contribution_audit_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_employer_contribution_audit(
            str(root / "data" / "processed" / "employer_contribution_audit.csv")
        )
        == []
    )


def test_employer_contribution_audit_requires_benchmark_debt_warning(tmp_path: Path) -> None:
    audit = tmp_path / "employer_contribution_audit.csv"
    audit.write_text(
        "year,employer_class,unit,price_basis,accounting_basis,legal_employer_rate_total,"
        "legal_due,recorded_cga_employer_revenue,timing_adjustments,arrears_corrections,"
        "base_definition_adjustment,perimeter_adjustment,legal_compliance_gap,"
        "economic_benchmark_rate_total,economic_benchmark_due,economic_benchmark_gap,"
        "source_ids,status,notes\n"
        "2011,class,EUR_million,current,basis,0.15,,,,,,,,0.2375,,,SRC,blocked,missing\n",
        encoding="utf-8",
    )

    errors = validate_employer_contribution_audit(str(audit))
    assert (
        "Employer contribution audit row 2 must state that the economic benchmark is "
        "not a legal debt" in errors
    )


def test_repository_state_financing_rule_registry_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_state_financing_rule_registry(
            str(root / "evidence" / "state_financing_rule_registry.csv"),
            str(root / "evidence" / "source_registry.csv"),
        )
        == []
    )


def test_state_financing_registry_rejects_misclassified_specific_transfer(
    tmp_path: Path,
) -> None:
    source_registry = tmp_path / "source_registry.csv"
    source_registry.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,title,institution,type,2012,url,url,2026-08-21,2012,basis,,,registered,notes\n",
        encoding="utf-8",
    )
    registry = tmp_path / "state_financing_rule_registry.csv"
    registry.write_text(
        "rule_id,valid_from,valid_to,institution,transfer_type,state_role,legal_basis,"
        "calculation_rule,recipient,accounting_basis,source_id,status,notes\n"
        "STATE,2012-01-01,,Social_Security,specific_state_transfer,budget_authority,"
        "law,specific State financing,Social_Security,basis,SRC,legal_rule_observed,"
        "transfer not evidence of underfunding by itself\n",
        encoding="utf-8",
    )

    errors = validate_state_financing_rule_registry(str(registry), str(source_registry))
    assert "Specific State transfer row STATE must use guarantor role" in errors
