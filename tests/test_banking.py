from pathlib import Path

import pytest

from portugal_pensions.banking import (
    actuarial_present_value_bounds,
    bank_transfer_balance,
    present_value,
    validate_actuarial_identifiability_registry,
    validate_bank_asset_liability_institution_requirements,
    validate_bank_asset_liability_outputs,
    validate_bank_asset_trace_controls,
    validate_bank_benefit_risk_classification_requirements,
    validate_bank_benefit_risk_distribution,
    validate_bank_esa_treatment_bridge,
    validate_bank_financial_statement_effects,
    validate_bank_pension_cost_2012,
    validate_bank_pension_transfer_registry,
    validate_bank_special_regime_annual,
    validate_bank_state_financing_reconciliation,
    validate_bank_transfer_debt_financing_effects,
    validate_bank_transfer_legal_coverage,
    validate_bank_worker_rgss_contributions,
    validate_bpn_2012_pension_transfer,
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


def test_actuarial_present_value_bounds_use_explicit_inputs() -> None:
    result = actuarial_present_value_bounds(
        cash_flow_lower=[90.0, 90.0],
        cash_flow_upper=[110.0, 110.0],
        annual_discount_rates=[0.02, 0.06],
    )

    assert result.lower_pv == pytest.approx(165.0)
    assert result.upper_pv == pytest.approx(213.6)
    assert result.precision_decimals == 1


def test_actuarial_present_value_bounds_reject_inverted_cashflow_bounds() -> None:
    with pytest.raises(ValueError, match="exceeds"):
        actuarial_present_value_bounds(
            cash_flow_lower=[120.0],
            cash_flow_upper=[100.0],
            annual_discount_rates=[0.04],
        )


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


def test_repository_bank_transfer_legal_coverage_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_transfer_legal_coverage(
            str(root / "data" / "processed" / "bank_transfer_legal_coverage.csv"),
            str(root / "evidence" / "bank_pension_transfer_registry.csv"),
        )
        == []
    )


def test_bank_transfer_legal_coverage_requires_dl127_fields(tmp_path: Path) -> None:
    coverage = tmp_path / "bank_transfer_legal_coverage.csv"
    registry = tmp_path / "bank_pension_transfer_registry.csv"
    coverage.write_text(
        "coverage_id,legal_source_id,instrument,requirement,registry_record_ids,"
        "coverage_status,limitation,notes\n"
        "C1,DR_DL127_2011,DL127,pensions_assumed,DL127_OBJECT_1,"
        "official_detail_registered,raw_pdf_not_acquired,notes\n",
        encoding="utf-8",
    )
    registry.write_text(
        "record_id,legal_source_id,instrument,publication_date,effective_date,category,"
        "article,subject,legal_rule,value,unit,status,notes\n"
        "DL127_OBJECT_1,DR_DL127_2011,DL127,2011-12-31,2011-12-31,"
        "pensions_assumed,Artigo 1,subject,rule,,,official_detail_registered,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_transfer_legal_coverage(str(coverage), str(registry))
    assert "Missing bank transfer legal source coverage: DR_DL54_2009" in errors
    assert "Missing DL127 legal coverage requirement: legal_discount_rate" in errors


def test_bank_transfer_legal_coverage_requires_all_institutions(tmp_path: Path) -> None:
    coverage = tmp_path / "bank_transfer_legal_coverage.csv"
    registry = tmp_path / "bank_pension_transfer_registry.csv"
    coverage.write_text(
        "coverage_id,legal_source_id,instrument,requirement,registry_record_ids,"
        "coverage_status,limitation,notes\n"
        "T1,DR_DL54_2009,DL54,timeline_event,R1,source_acquired,none,notes\n"
        "T2,DR_DL1A_2011,DL1A,timeline_event,R2,source_acquired,none,notes\n"
        "T3,DR_DL88_2012,DL88,timeline_event,R3,source_acquired,none,notes\n"
        "D1,DR_DL127_2011,DL127,pensions_assumed,R4,official_detail_registered,"
        "raw_pdf_not_acquired,notes\n"
        "D2,DR_DL127_2011,DL127,liabilities_retained_by_banks,R4,"
        "official_detail_registered,raw_pdf_not_acquired,notes\n"
        "D3,DR_DL127_2011,DL127,assets_transferred,R4,official_detail_registered,"
        "raw_pdf_not_acquired,notes\n"
        "D4,DR_DL127_2011,DL127,state_financing,R4,official_detail_registered,"
        "raw_pdf_not_acquired,notes\n"
        "D5,DR_DL127_2011,DL127,valuation_date,R4,official_detail_registered,"
        "raw_pdf_not_acquired,notes\n"
        "D6,DR_DL127_2011,DL127,legal_discount_rate,R4,official_detail_registered,"
        "raw_pdf_not_acquired,notes\n"
        "D7,DR_DL127_2011,DL127,mortality_tables,R4,official_detail_registered,"
        "raw_pdf_not_acquired,notes\n"
        "D8,DR_DL127_2011,DL127,independent_valuation_procedure,R4,"
        "official_detail_registered,raw_pdf_not_acquired,notes\n"
        "D9,DR_DL127_2011,DL127,asset_composition_constraints,R4,"
        "official_detail_registered,raw_pdf_not_acquired,notes\n"
        "D10,DR_DL127_2011,DL127,transfer_schedule,R4,official_detail_registered,"
        "raw_pdf_not_acquired,notes\n"
        "D11,DR_DL127_2011,DL127,participating_institutions,R4,"
        "official_detail_registered,raw_pdf_not_acquired,notes\n"
        "D12,DR_DL127_2011,DL127,extinguishing_covered_bank_liabilities,R4,"
        "official_detail_registered,raw_pdf_not_acquired,notes\n",
        encoding="utf-8",
    )
    registry.write_text(
        "record_id,legal_source_id,instrument,publication_date,effective_date,category,"
        "article,subject,legal_rule,value,unit,status,notes\n"
        "R1,SRC,DL,2009-01-01,2009-01-01,timeline,a,s,r,,,source_acquired,notes\n"
        "R2,SRC,DL,2011-01-01,2011-01-01,timeline,a,s,r,,,source_acquired,notes\n"
        "R3,SRC,DL,2012-01-01,2012-01-01,timeline,a,s,r,,,source_acquired,notes\n"
        "R4,SRC,DL,2011-12-31,2011-12-31,field,a,s,r,,,"
        "official_detail_registered,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_transfer_legal_coverage(str(coverage), str(registry))
    assert "Participating-institutions coverage must reference 18 registry records" in errors


def test_repository_bank_worker_rgss_contributions_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_worker_rgss_contributions(
            str(root / "data" / "processed" / "bank_worker_rgss_contributions.csv"),
            str(root / "data" / "processed" / "bank_worker_legal_population_mapping.csv"),
        )
        == []
    )


def test_bank_worker_rgss_contributions_require_core_populations(tmp_path: Path) -> None:
    contributions = tmp_path / "bank_worker_rgss_contributions.csv"
    mapping = tmp_path / "bank_worker_legal_population_mapping.csv"
    contributions.write_text(
        "record_id,year,population_id,legal_source_ids,legal_basis,contingency_scope,"
        "employee_contributions,employer_contributions,unit,accounting_basis,perimeter,"
        "separation_from_pension_transfer,reconciliation_source_ids,status,blocking_issue,"
        "notes\n"
        "R1,2009,new_bank_workers_rgss,DR_DL54_2009,legal,scope,,,"
        "EUR_million,cash,perimeter,not_pension_fund_assets,source,"
        "blocked_missing_official_flow_inputs,primary source missing,notes\n",
        encoding="utf-8",
    )
    mapping.write_text(
        "population_id,legal_source_id,instrument,effective_date,population,"
        "rgss_integration_status,covered_contingencies,retained_or_excluded_contingencies,"
        "relationship_to_2011_pension_transfer,source_registry_status,"
        "contribution_flow_status,notes\n"
        "new_bank_workers_rgss,DR_DL54_2009,DL54,2009-03-03,population,status,"
        "covered,retained,separate_not_pension_fund_asset,source_acquired,"
        "blocked_missing_official_flow_inputs,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_worker_rgss_contributions(str(contributions), str(mapping))
    assert (
        "Missing bank-worker contribution population: active_bank_workers_cafeb_integration"
        in errors
    )
    assert (
        "Missing bank-worker legal population mapping: pensioners_in_payment_dl127_excluded"
        in errors
    )


def test_bank_worker_rgss_contributions_reject_blocked_values(tmp_path: Path) -> None:
    contributions = tmp_path / "bank_worker_rgss_contributions.csv"
    mapping = tmp_path / "bank_worker_legal_population_mapping.csv"
    contributions.write_text(
        "record_id,year,population_id,legal_source_ids,legal_basis,contingency_scope,"
        "employee_contributions,employer_contributions,unit,accounting_basis,perimeter,"
        "separation_from_pension_transfer,reconciliation_source_ids,status,blocking_issue,"
        "notes\n"
        "R1,2009,new_bank_workers_rgss,DR_DL54_2009,legal,scope,1.0,,"
        "EUR_million,cash,perimeter,not_pension_fund_assets,source,"
        "blocked_missing_official_flow_inputs,primary source missing,notes\n"
        "R2,2011,active_bank_workers_cafeb_integration,DR_DL1A_2011,legal,scope,,,"
        "EUR_million,cash,perimeter,not_pension_fund_assets,source,"
        "blocked_missing_official_flow_inputs,primary source missing,notes\n"
        "R3,2011,pensioners_in_payment_dl127_excluded,DR_DL127_2011,legal,scope,,,"
        "not_applicable,legal,perimeter,excluded_from_contribution_flow,source,"
        "not_applicable,no contribution flow,notes\n",
        encoding="utf-8",
    )
    mapping.write_text(
        "population_id,legal_source_id,instrument,effective_date,population,"
        "rgss_integration_status,covered_contingencies,retained_or_excluded_contingencies,"
        "relationship_to_2011_pension_transfer,source_registry_status,"
        "contribution_flow_status,notes\n"
        "new_bank_workers_rgss,DR_DL54_2009,DL54,2009-03-03,population,status,"
        "covered,retained,separate_not_pension_fund_asset,source_acquired,"
        "blocked_missing_official_flow_inputs,notes\n"
        "active_bank_workers_cafeb_integration,DR_DL1A_2011,DL1A,2011-01-04,"
        "population,status,covered,retained,separate_not_pension_fund_asset,"
        "source_acquired,blocked_missing_official_flow_inputs,notes\n"
        "pensioners_in_payment_dl127_excluded,DR_DL127_2011,DL127,2011-12-31,"
        "population,status,covered,retained,pension_liability_not_pension_fund_asset,"
        "official_detail_registered,not_applicable,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_worker_rgss_contributions(str(contributions), str(mapping))
    assert (
        "Blocked bank-worker contribution rows must not contain contribution values on row 2"
        in errors
    )
    assert (
        "Bank-worker contribution rows must state they are not pension-fund assets on row 4"
        in errors
    )


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


def test_repository_bank_asset_liability_institution_requirements_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_asset_liability_institution_requirements(
            str(root / "data" / "processed" / "bank_asset_liability_institution_requirements.csv"),
            str(root / "data" / "processed" / "bank_asset_trace.csv"),
        )
        == []
    )


def test_repository_bank_asset_trace_controls_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_asset_trace_controls(
            str(root / "data" / "processed" / "bank_asset_trace_controls.csv")
        )
        == []
    )


def test_repository_actuarial_identifiability_registry_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_actuarial_identifiability_registry(
            str(root / "evidence" / "actuarial_identifiability_registry.csv")
        )
        == []
    )


def test_repository_bank_special_regime_annual_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_special_regime_annual(
            str(root / "evidence" / "bank_special_regime_annual.csv")
        )
        == []
    )


def test_repository_bank_state_financing_reconciliation_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_state_financing_reconciliation(
            str(root / "evidence" / "bank_special_regime_annual.csv"),
            str(root / "data" / "processed" / "bank_transfer_long_run.csv"),
            str(root / "evidence" / "bank_state_financing_reconciliation_requirements.csv"),
        )
        == []
    )


def test_repository_bank_benefit_risk_distribution_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_benefit_risk_distribution(
            str(root / "data" / "processed" / "bank_benefit_risk_distribution.csv")
        )
        == []
    )


def test_repository_bank_benefit_risk_classification_requirements_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_benefit_risk_classification_requirements(
            str(root / "evidence" / "bank_benefit_risk_classification_requirements.csv")
        )
        == []
    )


def test_repository_bank_financial_statement_effects_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_financial_statement_effects(
            str(root / "data" / "processed" / "bank_financial_statement_effects.csv"),
            str(root / "evidence" / "bank_financial_statement_source_evidence.csv"),
            str(root / "data" / "processed" / "bank_asset_liability_institution_requirements.csv"),
        )
        == []
    )


def test_repository_bank_esa_treatment_bridge_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_esa_treatment_bridge(
            str(root / "data" / "processed" / "bank_esa_treatment_bridge.csv")
        )
        == []
    )


def test_bank_esa_treatment_bridge_checks_percent_identity(tmp_path: Path) -> None:
    bridge = tmp_path / "bank_esa_treatment_bridge.csv"
    bridge.write_text(
        "record_id,year,transaction,esa_standard,classification,deficit_effect_direction,"
        "deficit_effect_percent_gdp,amount_eur_million,implied_gdp_eur_million,unit,"
        "source_ids,status,notes\n"
        "R1,2011,bank_pension_fund_transfer,ESA-95,revenue_increasing_operation,"
        "deficit_decreasing,10.0,50.0,1000.0,EUR_million,SRC,"
        "replicated_from_cge_and_ec,notes\n"
        "R2,2011,bank_pension_fund_transfer,ESA-2010,financial_transaction,"
        "no_direct_deficit_impact,0.0,,,EUR_million,SRC,"
        "classification_confirmed_from_ec,notes\n"
        "R3,2011,bank_pension_fund_transfer,bridge,bridge,not_applicable,,,,"
        "EUR_million,SRC,interpretive_bridge,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_esa_treatment_bridge(str(bridge))
    assert "Bank ESA bridge percent identity fails on row 2" in errors


def test_repository_bank_pension_cost_2012_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_pension_cost_2012(
            str(root / "data" / "processed" / "bank_pension_cost_2012.csv")
        )
        == []
    )


def test_bank_pension_cost_2012_checks_financing_residual(tmp_path: Path) -> None:
    cost = tmp_path / "bank_pension_cost_2012.csv"
    cost.write_text(
        "record_id,year,perimeter,measure,value_eur_million,benchmark_eur_million,"
        "residual_vs_benchmark_eur_million,unit,price_basis,accounting_basis,source_ids,"
        "status,notes\n"
        "R1,2012,perimeter,transfer_current_expenditure_pensions,516.0,500.0,16.0,"
        "EUR_million,current_prices,budgetary_public_accounts,SRC,"
        "official_account_reconciles_ec_approximation,notes\n"
        "R2,2012,perimeter,state_current_transfer_financing,515.0,,,EUR_million,"
        "current_prices,budgetary_public_accounts,SRC,official_account_extracted,notes\n"
        "R3,2012,perimeter,pension_expenditure_less_state_transfer,0.0,,,EUR_million,"
        "current_prices,budgetary_public_accounts,SRC,reconciled_same_report,notes\n"
        "R4,2012,perimeter,unresolved_component_split,,,,EUR_million,current_prices,"
        "budgetary_public_accounts,SRC,blocked_missing_component_split,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_pension_cost_2012(str(cost))
    assert "Bank pension cost financing residual identity fails" in errors


def test_repository_bank_transfer_debt_financing_effects_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bank_transfer_debt_financing_effects(
            str(root / "data" / "processed" / "bank_transfer_debt_financing_effects.csv")
        )
        == []
    )


def test_bank_transfer_debt_financing_effects_checks_interest_identity(
    tmp_path: Path,
) -> None:
    debt = tmp_path / "bank_transfer_debt_financing_effects.csv"
    debt.write_text(
        "record_id,year,perimeter,channel,asset_financing_effect_eur_million,"
        "pension_obligation_cost_eur_million,interest_rate,interest_cost_effect_eur_million,"
        "unit,price_basis,accounting_basis,source_ids,status,notes\n"
        "R1,2011,perimeter,recorded_2011_asset_receipt,3263.1,,,0.0,EUR_million,"
        "current_prices,budgetary_public_accounts,SRC,official_account_extract,notes\n"
        "R2,2011,perimeter,total_transfer_value,5993.2,,,0.0,EUR_million,"
        "current_prices,budgetary_public_accounts,SRC,aggregate_transfer_registered,notes\n"
        "R3,2011,perimeter,gross_debt_classification_gap,,,,,EUR_million,"
        "current_prices,public_debt_classification,SRC,blocked_missing_asset_composition,notes\n"
        "R4,2012,perimeter,pension_payment_cost,,516.0,,0.0,EUR_million,"
        "current_prices,budgetary_public_accounts,SRC,official_account_extract,notes\n"
        "R5,2012,perimeter,budgetary_financing_and_pension_payment,516.0,516.0,,0.0,"
        "EUR_million,current_prices,budgetary_public_accounts,SRC,reconciled_same_report,"
        "notes\n"
        "R6,2012,perimeter,interest_sensitivity_2011_receipt_programme_loan_rate,100.0,,"
        "0.026,-1.0,EUR_million,current_prices,sensitivity_observed_public_borrowing_cost,"
        "SRC,sensitivity_observed_rate,notes\n"
        "R7,2012,perimeter,interest_sensitivity_2011_receipt_implicit_debt_rate,100.0,,"
        "0.037,-3.7,EUR_million,current_prices,sensitivity_observed_public_borrowing_cost,"
        "SRC,sensitivity_observed_rate,notes\n"
        "R8,2012,perimeter,interest_sensitivity_2011_receipt_10y_treasury_yield,100.0,,"
        "0.073,-7.3,EUR_million,current_prices,sensitivity_observed_public_borrowing_cost,"
        "SRC,sensitivity_observed_rate,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_transfer_debt_financing_effects(str(debt))
    assert "Bank debt-financing interest identity fails on row 7" in errors


def test_repository_bpn_2012_pension_transfer_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_bpn_2012_pension_transfer(
            str(root / "data" / "processed" / "bpn_2012_pension_transfer.csv")
        )
        == []
    )


def test_bpn_2012_pension_transfer_requires_panel_exclusion(tmp_path: Path) -> None:
    transfer = tmp_path / "bpn_2012_pension_transfer.csv"
    transfer.write_text(
        "record_id,year,case_id,measure,value,unit,receiving_institution,payment_institution,"
        "population,perimeter_inclusion,accounting_basis,source_ids,status,notes\n"
        "R1,2012,bpn_group_dl88,active_worker_rgss_integration,,not_applicable,RGSS,,"
        "workers,bpn_separate_case,legal_scope,SRC,legal_scope_registered,notes\n"
        "R2,2012,bpn_group_dl88,cga_responsibility_current_pensions,,not_applicable,CGA,"
        "ISS_CNP,pensioners,bpn_separate_case,legal_scope,SRC,legal_scope_registered,notes\n"
        "R3,2012,bpn_group_dl88,cga_responsibility_future_benefits,,not_applicable,CGA,"
        "ISS_CNP,workers,bpn_separate_case,legal_scope,SRC,legal_scope_registered,notes\n"
        "R4,2012,bpn_group_dl88,asset_transfer_to_cga,96.768004,EUR_million,CGA,,"
        "responsibilities,bpn_separate_case,legal_transfer_value,SRC,"
        "official_legal_amount_extracted,notes\n"
        "R5,2012,bpn_group_dl88,sams_assets_returned_to_entities,7.319430,EUR_million,"
        "BPN_group_entities,,sams,bpn_separate_case,legal_transfer_value,SRC,"
        "official_legal_amount_extracted,notes\n"
        "R6,2012,bpn_group_dl88,cga_financing_to_ss_2012,0.1359,EUR_million,CGA,"
        "ISS_CNP,component,bpn_separate_case,budgetary_public_accounts,SRC,"
        "official_account_extract,notes\n"
        "R7,2012,bpn_group_dl88,pensioners_2012,11,count,CGA,,pensioners,"
        "bpn_separate_case,cga_accounts,SRC,official_account_extract,notes\n"
        "R8,2012,bpn_group_dl88,survivor_pensioners_2012,18,count,CGA,,survivors,"
        "bpn_separate_case,cga_accounts,SRC,official_account_extract,notes\n"
        "R9,2012,bpn_group_dl88,pensions_paid_by_cga_fund_2012,0.17927,EUR_million,CGA,,"
        "payments,bpn_separate_case,cga_accounts,SRC,official_account_extract,notes\n"
        "R10,2012,bpn_group_dl88,main_2011_panel_inclusion,,not_applicable,CGA,ISS_CNP,"
        "population,included_in_2011_dl127_panel,perimeter_classification,SRC,"
        "panel_boundary_registered,notes\n",
        encoding="utf-8",
    )

    errors = validate_bpn_2012_pension_transfer(str(transfer))
    assert "BPN case must remain excluded from the main 2011 DL127 panel" in errors


def test_bank_benefit_risk_distribution_blocks_subsidy_without_values(tmp_path: Path) -> None:
    distribution = tmp_path / "bank_benefit_risk_distribution.csv"
    distribution.write_text(
        "record_id,year,institution,channel,value,unit,price_basis,accounting_basis,"
        "bank_effect,public_sector_effect,risk_holder_after_transfer,source_ids,status,notes\n"
        "R1,2011,aggregate,demonstrable_net_subsidy,10,EUR_million,current_prices,"
        "economic_valuation,bank,public,unclassified,SRC,complete,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_benefit_risk_distribution(str(distribution))
    assert "Expected 18 bank-level net-position rows, found 0" in errors
    assert "Demonstrable net-subsidy row must not have a value while blocked" in errors
    assert "Demonstrable net-subsidy row must remain blocked" in errors


def test_bank_benefit_risk_requirements_block_subsidy_inference(tmp_path: Path) -> None:
    requirements = tmp_path / "bank_benefit_risk_classification_requirements.csv"
    requirements.write_text(
        "requirement_id,classification_target,required_inputs,available_inputs,"
        "permitted_output,status,blocking_issue,notes\n"
        "REQ1,demonstrable_net_subsidy,liability_derecognized,legal rule,"
        "classify_from_liability_transfer,complete,records missing,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_benefit_risk_classification_requirements(str(requirements))
    assert "Missing bank benefit-risk classification target: bank_level_net_position" in errors
    assert "Unexpected bank benefit-risk requirement status on row 2" in errors
    assert "Missing subsidy classification input bank_level_net_position on row 2" in errors
    assert "Subsidy classification requirement must block inference on row 2" in errors


def test_bank_special_regime_annual_checks_residual_identity(tmp_path: Path) -> None:
    ledger = tmp_path / "bank_special_regime_annual.csv"
    ledger.write_text(
        "year,perimeter,unit,price_basis,accounting_basis,state_specific_transfer,"
        "pension_expenditure,administrative_cost,attributable_investment_income,"
        "asset_drawdown,other_financing,timing_adjustment,reconciliation_residual,"
        "source_ids,status,notes\n"
        "2012,transferred_bank_pensions,EUR_million,current_prices,budgetary_public_accounts,"
        "90,100,5,0,0,0,0,99,SRC,complete,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_special_regime_annual(str(ledger), end_year=2012)
    assert "Bank special-regime residual identity fails on row 2" in errors


def test_bank_state_financing_reconciliation_blocks_loss_classification(
    tmp_path: Path,
) -> None:
    annual = tmp_path / "bank_special_regime_annual.csv"
    long_run = tmp_path / "bank_transfer_long_run.csv"
    requirements = tmp_path / "bank_state_financing_reconciliation_requirements.csv"
    annual.write_text(
        "year,perimeter,unit,price_basis,accounting_basis,state_specific_transfer,"
        "pension_expenditure,administrative_cost,attributable_investment_income,"
        "asset_drawdown,other_financing,timing_adjustment,reconciliation_residual,"
        "source_ids,status,notes\n"
        "2012,perimeter,EUR_million,current_prices,budgetary_public_accounts,"
        "100,100,0,0,0,0,0,0,SRC,complete,notes\n",
        encoding="utf-8",
    )
    long_run.write_text(
        "year,perimeter,unit,price_basis,accounting_basis,state_specific_transfer,"
        "pension_expenditure,administrative_cost,attributable_investment_income,"
        "asset_drawdown,other_financing,timing_adjustment,reconciliation_residual,"
        "source_ids,status,notes\n"
        "2012,perimeter,EUR_million,current_prices,budgetary_public_accounts,"
        "100,101,0,0,0,0,0,1,SRC,complete,notes\n",
        encoding="utf-8",
    )
    requirements.write_text(
        "requirement_id,component,period,required_source,observed_evidence,"
        "allowed_use,status,blocking_issue,notes\n"
        "REQ1,reconciliation_residual,2012-2025,source,observed,"
        "classify_as_social_security_loss,blocked_missing_full_component_set,"
        "primary records missing,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_state_financing_reconciliation(
        str(annual),
        str(long_run),
        str(requirements),
        end_year=2012,
    )
    assert "Bank special-regime annual and long-run ledgers must match exactly" in errors
    assert (
        "Bank State-financing residual requirement must block loss classification on row 2"
        in errors
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


def test_bank_asset_liability_requirements_match_trace_institutions(tmp_path: Path) -> None:
    requirements = tmp_path / "bank_asset_liability_institution_requirements.csv"
    trace = tmp_path / "bank_asset_trace.csv"
    requirements.write_text(
        "requirement_id,institution,legal_source_id,required_liability_fields,"
        "required_asset_fields,statutory_equality_status,sensitivity_status,"
        "economic_interpretation_rule,status,blocking_issue,notes\n"
        "REQ1,Bank A,DR_DL127_2011,final_actuarial_liability_pv_legal_4pct;"
        "cashflow_schedule,final_assets_transferred_total;cash_transferred;"
        "portuguese_public_debt_transferred;other_assets_transferred;final_adjustment,"
        "statutory_equality_not_reproduced_missing_inputs,"
        "sensitivity_blocked_missing_cashflows,"
        "alternative_discount_rate_is_sensitivity_not_underfunding_finding,"
        "blocked_missing_bank_level_values,primary schedules missing,notes\n",
        encoding="utf-8",
    )
    trace.write_text(
        "institution,asset_type,transfer_value,destination,accounting_treatment,source_id,"
        "status,notes\n"
        "Bank A,final_assets_transferred,,State,treatment,SRC,"
        "blocked_missing_bank_level_values,notes\n"
        "Bank B,final_assets_transferred,,State,treatment,SRC,"
        "blocked_missing_bank_level_values,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_asset_liability_institution_requirements(
        str(requirements),
        str(trace),
    )
    assert "Expected 18 bank asset-liability institution requirements, found 1" in errors
    assert "Missing bank asset-liability institution requirement: Bank B" in errors


def test_bank_asset_liability_requirements_block_underfunding_language(
    tmp_path: Path,
) -> None:
    requirements = tmp_path / "bank_asset_liability_institution_requirements.csv"
    trace = tmp_path / "bank_asset_trace.csv"
    requirements.write_text(
        "requirement_id,institution,legal_source_id,required_liability_fields,"
        "required_asset_fields,statutory_equality_status,sensitivity_status,"
        "economic_interpretation_rule,status,blocking_issue,notes\n"
        "REQ1,Bank A,DR_DL127_2011,final_actuarial_liability_pv_legal_4pct,"
        "final_assets_transferred_total,complete,complete,underfunded,"
        "blocked_missing_bank_level_values,primary schedules missing,notes\n",
        encoding="utf-8",
    )
    trace.write_text(
        "institution,asset_type,transfer_value,destination,accounting_treatment,source_id,"
        "status,notes\n"
        "Bank A,final_assets_transferred,,State,treatment,SRC,"
        "blocked_missing_bank_level_values,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_asset_liability_institution_requirements(
        str(requirements),
        str(trace),
    )
    assert "Missing liability requirement cashflow_schedule on row 2" in errors
    assert "Missing asset requirement cash_transferred on row 2" in errors
    assert "Unexpected statutory equality status on row 2" in errors
    assert (
        "Bank asset-liability requirement must block underfunding interpretation on row 2" in errors
    )


def test_bank_asset_trace_controls_block_ring_fenced_assumptions(tmp_path: Path) -> None:
    controls = tmp_path / "bank_asset_trace_controls.csv"
    controls.write_text(
        "control_id,trace_scope,required_evidence,observed_evidence,"
        "ownership_destination,accounting_treatment,composition_status,"
        "ring_fence_status,permitted_long_run_use,status,blocking_issue,"
        "source_ids,notes\n"
        "C1,recorded_2011_state_receipt,required,3263.1 EUR_million,"
        "Social Security,treatment,aggregate_only,social_security_ring_fenced,"
        "attribute_social_security_asset_income,partial_aggregate_extract,"
        "records missing,SRC,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_asset_trace_controls(str(controls))
    assert "Missing bank asset trace control scope: cash_component" in errors
    assert "Bank asset trace control row 2 must assign assets to State" in errors
    assert (
        "Bank asset trace controls must block Social Security or FEFSS ring-fence "
        "assumptions on row 2"
    ) in errors
    assert (
        "Bank asset trace controls must not attribute investment income to Social Security on row 2"
    ) in errors


def test_bank_financial_statement_effects_require_net_measured_channel(
    tmp_path: Path,
) -> None:
    effects = tmp_path / "bank_financial_statement_effects.csv"
    sources = tmp_path / "bank_financial_statement_source_evidence.csv"
    requirements = tmp_path / "bank_asset_liability_institution_requirements.csv"
    effects.write_text(
        "institution,year,liability_derecognized,assets_surrendered,gain_loss,"
        "capital_effect,retained_obligations,measurable_channel,net_value,unit,"
        "source_id,status,notes\n"
        "Bank A,2011,100,,,,,liability_derecognized,,EUR_million,SRC,complete,"
        "notes\n",
        encoding="utf-8",
    )
    sources.write_text(
        "source_record_id,institution,years_required,required_documents,source_locator,"
        "acquisition_status,extraction_status,required_fields,merger_resolution_flag,"
        "blocking_issue,notes\n"
        "SRC1,Bank A,2011;2012,annual report,locator,acquired,extracted,"
        "liability_derecognized;assets_surrendered;gain_loss;capital_effect;"
        "retained_obligations;accounting_policy_note,none,none,notes\n",
        encoding="utf-8",
    )
    requirements.write_text(
        "requirement_id,institution,legal_source_id,required_liability_fields,"
        "required_asset_fields,statutory_equality_status,sensitivity_status,"
        "economic_interpretation_rule,status,blocking_issue,notes\n"
        "REQ1,Bank A,DR_DL127_2011,final_actuarial_liability_pv_legal_4pct,"
        "final_assets_transferred_total,blocked,blocked,blocked,"
        "blocked_missing_bank_level_values,primary schedules missing,notes\n",
        encoding="utf-8",
    )

    errors = validate_bank_financial_statement_effects(
        str(effects),
        str(sources),
        str(requirements),
    )
    assert "Measured bank financial statement rows must include net_value on row 2" in errors
    assert (
        "Gross liability extinguishment is not a sufficient measurable channel on row 2" in errors
    )
    assert "Bank financial statement effects must cover 2011 and 2012 for Bank A" in errors


def test_actuarial_identifiability_blocks_false_precision(tmp_path: Path) -> None:
    registry = tmp_path / "actuarial_identifiability_registry.csv"
    registry.write_text(
        "record_id,quantity,valuation_target,required_inputs,available_inputs,"
        "identifiability,status,permitted_method,precision_rule,sensitivity_dimension,"
        "blocking_issue,notes\n"
        "R1,discount_rate_sensitivity,target,cash_flow_schedule,grid,"
        "not_identified_without_cashflows,complete,point_estimate,exact_point_estimate,"
        "discount_rate,inputs missing,notes\n"
        "R2,underfunding_classification,target,cash_flow_schedule,grid,"
        "not_identified_without_full_transfer_panel,blocked_missing_full_panel,"
        "classification_blocked,no_point_estimate,interpretation,"
        "primary inputs missing,notes\n",
        encoding="utf-8",
    )

    errors = validate_actuarial_identifiability_registry(str(registry))
    assert "Missing actuarial identifiability dimension: longevity" in errors
    assert "Actuarial identifiability row 2 must remain blocked" in errors
    assert (
        "Actuarial identifiability precision rule must not allow unsupported point "
        "estimates on row 2"
    ) in errors
    assert (
        "Actuarial interpretation row must block alternative-rate underfunding language" in errors
    )
