from pathlib import Path

import pytest

from portugal_pensions.counterfactuals import (
    capitalize_cash_flows,
    compound_reserve,
    funding_substitution,
    public_worker_reallocation_flow,
    validate_counterfactual_financing_regimes,
    validate_fefss_return_inputs,
    validate_public_worker_liability_assumptions,
    validate_public_worker_reallocation,
    validate_public_worker_reallocation_bridge,
)


def test_compound_reserve() -> None:
    path = compound_reserve([100.0, 100.0], [0.10, 0.10])
    assert path == pytest.approx([110.0, 231.0])


def test_capitalize_cash_flows_timing_conventions() -> None:
    assert capitalize_cash_flows([100.0], [0.21], timing="beginning") == pytest.approx([121.0])
    assert capitalize_cash_flows([100.0], [0.21], timing="mid") == pytest.approx([110.0])
    assert capitalize_cash_flows([100.0], [0.21], timing="end") == pytest.approx([100.0])


def test_funding_substitution_does_not_create_extra_cash() -> None:
    employer, state = funding_substitution(100.0, 40.0)
    assert employer + state == pytest.approx(100.0)


def test_public_worker_reallocation_flow_identity() -> None:
    employee, employer, total = public_worker_reallocation_flow(1000.0, 0.11, 0.2375)
    assert employee == pytest.approx(110.0)
    assert employer == pytest.approx(237.5)
    assert total == pytest.approx(347.5)


def test_repository_public_worker_reallocation_files_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_public_worker_reallocation(
            str(root / "data" / "processed" / "public_worker_rgss_cohorts.csv"),
            str(root / "data" / "processed" / "public_worker_rgss_contributions_2006_2025.csv"),
        )
        == []
    )


def test_repository_public_worker_reallocation_bridge_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_public_worker_reallocation_bridge(
            str(root / "data" / "processed" / "public_worker_reallocation_bridge.csv"),
            str(root / "evidence" / "source_registry.csv"),
        )
        == []
    )


def test_repository_public_worker_liability_assumptions_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_public_worker_liability_assumptions(
            str(root / "evidence" / "public_worker_liability_assumptions.csv"),
            str(root / "evidence" / "source_registry.csv"),
        )
        == []
    )


def test_repository_fefss_return_inputs_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_fefss_return_inputs(
            str(root / "data" / "processed" / "fefss_returns.csv"),
            str(root / "data" / "processed" / "public_worker_fefss_counterfactual.csv"),
            str(root / "evidence" / "source_registry.csv"),
            str(root / "data" / "processed" / "public_worker_fefss_sensitivity.csv"),
        )
        == []
    )


def test_repository_counterfactual_financing_regimes_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_counterfactual_financing_regimes(
            str(root / "evidence" / "counterfactual_registry.csv"),
            str(root / "data" / "processed" / "counterfactual_financing_regimes.csv"),
        )
        == []
    )


def test_counterfactual_regimes_require_registered_scenario_coverage(tmp_path: Path) -> None:
    registry = tmp_path / "counterfactual_registry.csv"
    regimes = tmp_path / "counterfactual_financing_regimes.csv"
    registry.write_text(
        "scenario_id,name,description,legal_or_economic,assumptions,status\n"
        "CF1,Scenario,Description,legal,Assumption,preregistered\n"
        "CF2,Scenario,Description,economic,Assumption,preregistered\n",
        encoding="utf-8",
    )
    regimes.write_text(
        "scenario_id,scenario_name,component,year_start,year_end,perimeter,"
        "stock_flow_treatment,financing_source_adjustment,required_input_dataset,"
        "implemented_function,value,unit,source_ids,status,notes\n"
        "CF1,Scenario,component,2006,2025,perimeter,cash_flow_counterfactual,"
        "adjustment,dataset,not_applicable,,EUR_million,SRC,blocked,notes\n",
        encoding="utf-8",
    )

    assert (
        "Registered counterfactual scenario is missing from regimes: CF2"
        in validate_counterfactual_financing_regimes(str(registry), str(regimes))
    )


def test_funded_reserve_rule_requires_additional_expenditure(tmp_path: Path) -> None:
    registry = tmp_path / "counterfactual_registry.csv"
    regimes = tmp_path / "counterfactual_financing_regimes.csv"
    registry.write_text(
        "scenario_id,name,description,legal_or_economic,assumptions,status\n"
        "CF3,Funded reserve,Description,economic,Assumption,preregistered\n",
        encoding="utf-8",
    )
    regimes.write_text(
        "scenario_id,scenario_name,component,year_start,year_end,perimeter,"
        "stock_flow_treatment,financing_source_adjustment,required_input_dataset,"
        "implemented_function,value,unit,source_ids,status,notes\n"
        "CF3,Funded reserve,component,2006,2025,perimeter,flow_then_stock,"
        "no offset,dataset,compound_reserve,,EUR_million,SRC,blocked,missing\n",
        encoding="utf-8",
    )

    assert (
        "CF3 must record funded-reserve contributions as additional expenditure"
        in validate_counterfactual_financing_regimes(str(registry), str(regimes))
    )


def test_public_worker_reallocation_requires_full_year_coverage(tmp_path: Path) -> None:
    cohorts = tmp_path / "cohorts.csv"
    contributions = tmp_path / "contributions.csv"
    cohorts.write_text(
        "year,cohort,lower,central,upper,unit,source_ids,status,notes\n"
        "2006,cohort,,,,workers,SRC,blocked,missing\n",
        encoding="utf-8",
    )
    contributions.write_text(
        "year,employee_contributions_lower,employee_contributions_central,"
        "employee_contributions_upper,employer_contributions_lower,"
        "employer_contributions_central,employer_contributions_upper,"
        "aggregate_rgss_contributions,unit,aggregate_unit,source_ids,"
        "observation_type,estimation_method,pension_related_basis,uncertainty_basis,"
        "aggregate_cap_status,status,missing_inputs,claim_permitted,notes\n"
        "2006,,,,,,,,EUR_million,EUR_million,SRC,mechanical_reallocation,"
        "blocked_source_gap,blocked_not_decomposed,missing,"
        "aggregate_cap_not_reconstructed,blocked,"
        "public_worker_new_entrant_counts;contribution_base_payroll;"
        "applicable_rgss_worker_rate;applicable_rgss_employer_rate;"
        "aggregate_rgss_contribution_revenue,no,missing\n",
        encoding="utf-8",
    )

    errors = validate_public_worker_reallocation(str(cohorts), str(contributions))
    assert "public worker cohort table must cover every year from 2006 to 2025" in errors


def test_public_worker_contributions_require_estimation_method(tmp_path: Path) -> None:
    cohorts = tmp_path / "cohorts.csv"
    contributions = tmp_path / "contributions.csv"
    cohorts.write_text(
        "year,cohort,lower,central,upper,unit,source_ids,status,notes\n"
        + "".join(
            f"{year},cohort,1,1,1,workers,SRC,complete,observed\n" for year in range(2006, 2026)
        ),
        encoding="utf-8",
    )
    contributions.write_text(
        "year,employee_contributions_lower,employee_contributions_central,"
        "employee_contributions_upper,employer_contributions_lower,"
        "employer_contributions_central,employer_contributions_upper,"
        "aggregate_rgss_contributions,unit,aggregate_unit,source_ids,"
        "observation_type,estimation_method,pension_related_basis,uncertainty_basis,"
        "aggregate_cap_status,status,missing_inputs,claim_permitted,notes\n"
        + "".join(
            f"{year},1,1,1,1,1,1,10,EUR_million,EUR_million,SRC,"
            "mechanical_reallocation,model,pension_related_rate,base_assumption,"
            "checked_against_aggregate_rgss_revenue,estimated,,yes,estimate\n"
            for year in range(2006, 2026)
        ),
        encoding="utf-8",
    )

    errors = validate_public_worker_reallocation(str(cohorts), str(contributions))
    assert (
        "Estimated public worker contribution rows must identify direct observation or "
        "reconstruction on row 2" in errors
    )


def test_public_worker_contributions_cannot_exceed_aggregate_rgss_revenue(
    tmp_path: Path,
) -> None:
    cohorts = tmp_path / "cohorts.csv"
    contributions = tmp_path / "contributions.csv"
    cohorts.write_text(
        "year,cohort,lower,central,upper,unit,source_ids,status,notes\n"
        + "".join(
            f"{year},cohort,1,1,1,workers,SRC,complete,observed\n" for year in range(2006, 2026)
        ),
        encoding="utf-8",
    )
    contributions.write_text(
        "year,employee_contributions_lower,employee_contributions_central,"
        "employee_contributions_upper,employer_contributions_lower,"
        "employer_contributions_central,employer_contributions_upper,"
        "aggregate_rgss_contributions,unit,aggregate_unit,source_ids,"
        "observation_type,estimation_method,pension_related_basis,uncertainty_basis,"
        "aggregate_cap_status,status,missing_inputs,claim_permitted,notes\n"
        + "".join(
            f"{year},4,5,6,4,5,6,9,EUR_million,EUR_million,SRC,"
            "mechanical_reallocation,reconstruction,pension_related_rate,"
            "base_assumption,checked_against_aggregate_rgss_revenue,estimated,,yes,"
            "estimate\n"
            for year in range(2006, 2026)
        ),
        encoding="utf-8",
    )

    errors = validate_public_worker_reallocation(str(cohorts), str(contributions))
    assert "Public worker contribution estimate exceeds aggregate RGSS revenue on row 2" in errors


def test_public_worker_reallocation_bridge_blocks_claims_without_inputs(tmp_path: Path) -> None:
    source_registry = tmp_path / "source_registry.csv"
    source_registry.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,Source,Institution,official,2006,url,url,2026-08-21,2006,cash,,,,notes\n",
        encoding="utf-8",
    )
    bridge = tmp_path / "bridge.csv"
    bridge.write_text(
        "year,mechanism,flow_component,worker_count,contribution_base,worker_rate,"
        "employer_rate,employee_contributions,employer_contributions,total_contributions,"
        "unit,price_basis,accounting_basis,excluded_effects,source_ids,status,"
        "missing_inputs,claim_permitted,notes\n"
        "2006,post_2006_cga_closure_new_entrants_to_rgss,mechanical_reallocation,"
        ",,,,,,,EUR_million,current_prices,cash_contribution_flow,"
        "demographic_change;wage_growth;general_labour_market_effects,SRC,"
        "blocked_missing_public_employment_payroll,"
        "public_worker_new_entrant_counts;contribution_base_payroll;"
        "applicable_rgss_worker_rate;applicable_rgss_employer_rate,yes,missing\n",
        encoding="utf-8",
    )

    errors = validate_public_worker_reallocation_bridge(str(bridge), str(source_registry))
    assert (
        "Blocked public worker reallocation bridge rows must not permit claims on row 2" in errors
    )


def test_public_worker_reallocation_bridge_checks_arithmetic_residual(tmp_path: Path) -> None:
    bridge = tmp_path / "bridge.csv"
    bridge.write_text(
        "year,mechanism,flow_component,worker_count,contribution_base,worker_rate,"
        "employer_rate,employee_contributions,employer_contributions,total_contributions,"
        "unit,price_basis,accounting_basis,excluded_effects,source_ids,status,"
        "missing_inputs,claim_permitted,notes\n"
        "2006,post_2006_cga_closure_new_entrants_to_rgss,mechanical_reallocation,"
        "10,1000,0.11,0.2375,110,237.5,300,EUR_million,current_prices,"
        "cash_contribution_flow,demographic_change;wage_growth;"
        "general_labour_market_effects,SRC,complete,,yes,complete\n",
        encoding="utf-8",
    )

    errors = validate_public_worker_reallocation_bridge(str(bridge))
    assert "Total contribution residual on public worker reallocation bridge row 2" in errors


def test_public_worker_liability_assumptions_block_free_sustainability_claims(
    tmp_path: Path,
) -> None:
    assumptions = tmp_path / "public_worker_liability_assumptions.csv"
    assumptions.write_text(
        "assumption_id,scope,period_start,period_end,current_flow_dataset,rights_measure,"
        "liability_measurement_basis,discount_rate_basis,mortality_basis,indexation_basis,"
        "microdata_status,aggregate_bounds_status,required_inputs,source_ids,status,"
        "claim_constraint,notes\n"
        "PWR1,scope,2006,2025,"
        "data/processed/public_worker_rgss_contributions_2006_2025.csv,"
        "accrued_rgss_pension_rights,basis,rate,mortality,indexation,missing_microdata,"
        "missing_bounds,cohort_counts;contribution_bases;service_histories;"
        "benefit_formula;indexation_rule;mortality_table;discount_rate,SRC,"
        "blocked_missing_liability_inputs,contributions improve cash flow,missing\n",
        encoding="utf-8",
    )

    errors = validate_public_worker_liability_assumptions(str(assumptions))
    assert (
        "public worker liability assumptions must block free-sustainability claims "
        "without pension-rights caveats on row 2" in errors
    )


def test_public_worker_liability_assumptions_require_actuarial_inputs(
    tmp_path: Path,
) -> None:
    assumptions = tmp_path / "public_worker_liability_assumptions.csv"
    assumptions.write_text(
        "assumption_id,scope,period_start,period_end,current_flow_dataset,rights_measure,"
        "liability_measurement_basis,discount_rate_basis,mortality_basis,indexation_basis,"
        "microdata_status,aggregate_bounds_status,required_inputs,source_ids,status,"
        "claim_constraint,notes\n"
        "PWR1,scope,2006,2025,"
        "data/processed/public_worker_rgss_contributions_2006_2025.csv,"
        "accrued_rgss_pension_rights,basis,rate,mortality,indexation,missing_microdata,"
        "missing_bounds,cohort_counts;contribution_bases,SRC,"
        "blocked_missing_liability_inputs,not a free gain because pension rights accrue,"
        "missing\n",
        encoding="utf-8",
    )

    errors = validate_public_worker_liability_assumptions(str(assumptions))
    assert (
        "public worker liability assumption row is missing required actuarial inputs on row 2"
        in errors
    )


def test_fefss_returns_require_full_year_coverage(tmp_path: Path) -> None:
    returns = tmp_path / "fefss_returns.csv"
    capitalization = tmp_path / "capitalization.csv"
    returns.write_text(
        "year,reported_return,return_type,valuation_basis,fees_basis,nominal_real_basis,"
        "source_ids,page,status,missing_inputs,notes\n"
        "2006,,,,,,SRC,,blocked_missing_official_return_series,"
        "official_annual_return;return_type;valuation_basis;fees_basis,missing\n",
        encoding="utf-8",
    )
    capitalization.write_text(
        "scenario_id,year,cash_flow,timing,annual_return,reserve_value,unit,source_ids,"
        "actual_fefss_assets,comparison_ratio,price_basis,nominal_real_basis,return_source,"
        "benchmark_source,financing_assumption,retained_resources_required,"
        "offsetting_financing_assumption,status,missing_inputs,claim_permitted,notes\n"
        "BEGIN,2006,,beginning,,,EUR_million,SRC,,,current_prices,nominal,returns,"
        "assets,additional_retained_resources_required,yes,,blocked,"
        "cash_flow;annual_return,no,missing\n"
        "MID,2006,,mid,,,EUR_million,SRC,,,current_prices,nominal,returns,assets,"
        "additional_retained_resources_required,yes,,blocked,cash_flow;annual_return,"
        "no,missing\n"
        "END,2006,,end,,,EUR_million,SRC,,,current_prices,nominal,returns,assets,"
        "additional_retained_resources_required,yes,,blocked,cash_flow;annual_return,"
        "no,missing\n",
        encoding="utf-8",
    )

    errors = validate_fefss_return_inputs(str(returns), str(capitalization))
    assert "FEFSS returns must cover every year from 2006 to 2025" in errors


def test_fefss_capitalization_requires_all_timing_conventions(tmp_path: Path) -> None:
    returns = tmp_path / "fefss_returns.csv"
    capitalization = tmp_path / "capitalization.csv"
    returns.write_text(
        "year,reported_return,return_type,valuation_basis,fees_basis,nominal_real_basis,"
        "source_ids,page,status,missing_inputs,notes\n"
        + "".join(
            f"{year},,,,,,SRC,,blocked_missing_official_return_series,"
            "official_annual_return;return_type;valuation_basis;fees_basis,missing\n"
            for year in range(2006, 2026)
        ),
        encoding="utf-8",
    )
    capitalization.write_text(
        "scenario_id,year,cash_flow,timing,annual_return,reserve_value,unit,source_ids,"
        "actual_fefss_assets,comparison_ratio,price_basis,nominal_real_basis,return_source,"
        "benchmark_source,financing_assumption,retained_resources_required,"
        "offsetting_financing_assumption,status,missing_inputs,claim_permitted,notes\n"
        "BEGIN,2006,,beginning,,,EUR_million,SRC,,,current_prices,nominal,returns,"
        "assets,additional_retained_resources_required,yes,,blocked,"
        "cash_flow;annual_return,no,missing\n",
        encoding="utf-8",
    )

    errors = validate_fefss_return_inputs(str(returns), str(capitalization))
    assert "FEFSS capitalization must include beginning mid and end timing rows" in errors


def test_fefss_capitalization_requires_retained_resources_or_offset(
    tmp_path: Path,
) -> None:
    returns = tmp_path / "fefss_returns.csv"
    capitalization = tmp_path / "capitalization.csv"
    returns.write_text(
        "year,reported_return,return_type,valuation_basis,fees_basis,nominal_real_basis,"
        "source_ids,page,status,missing_inputs,notes\n"
        + "".join(
            f"{year},,,,,,SRC,,blocked_missing_official_return_series,"
            "official_annual_return;return_type;valuation_basis;fees_basis,missing\n"
            for year in range(2006, 2026)
        ),
        encoding="utf-8",
    )
    capitalization.write_text(
        "scenario_id,year,cash_flow,timing,annual_return,reserve_value,unit,source_ids,"
        "actual_fefss_assets,comparison_ratio,price_basis,nominal_real_basis,return_source,"
        "benchmark_source,financing_assumption,retained_resources_required,"
        "offsetting_financing_assumption,status,missing_inputs,claim_permitted,notes\n"
        "BEGIN,2025,,beginning,,,EUR_million,SRC,,,current_prices,nominal,returns,assets,"
        "unspecified,no,,blocked,cash_flow;annual_return,no,missing\n"
        "MID,2025,,mid,,,EUR_million,SRC,,,current_prices,nominal,returns,assets,"
        "additional_retained_resources_required,yes,,blocked,cash_flow;annual_return,"
        "no,missing\n"
        "END,2025,,end,,,EUR_million,SRC,,,current_prices,nominal,returns,assets,"
        "additional_retained_resources_required,yes,,blocked,cash_flow;annual_return,"
        "no,missing\n",
        encoding="utf-8",
    )

    errors = validate_fefss_return_inputs(str(returns), str(capitalization))
    assert (
        "FEFSS capitalization rows must require retained resources unless an offsetting "
        "financing assumption is specified on row 2" in errors
    )
