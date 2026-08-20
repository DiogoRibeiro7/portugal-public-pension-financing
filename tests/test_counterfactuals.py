from pathlib import Path

import pytest

from portugal_pensions.counterfactuals import (
    compound_reserve,
    funding_substitution,
    validate_counterfactual_financing_regimes,
    validate_public_worker_reallocation,
)


def test_compound_reserve() -> None:
    path = compound_reserve([100.0, 100.0], [0.10, 0.10])
    assert path == pytest.approx([110.0, 231.0])


def test_funding_substitution_does_not_create_extra_cash() -> None:
    employer, state = funding_substitution(100.0, 40.0)
    assert employer + state == pytest.approx(100.0)


def test_repository_public_worker_reallocation_files_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_public_worker_reallocation(
            str(root / "data" / "processed" / "public_worker_rgss_cohorts.csv"),
            str(root / "data" / "processed" / "public_worker_rgss_contributions_2006_2025.csv"),
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
        "employer_contributions_central,employer_contributions_upper,unit,source_ids,"
        "observation_type,status,notes\n"
        "2006,,,,,,,EUR_million,SRC,mechanical_reallocation,blocked,missing\n",
        encoding="utf-8",
    )

    errors = validate_public_worker_reallocation(str(cohorts), str(contributions))
    assert "public worker cohort table must cover every year from 2006 to 2025" in errors
