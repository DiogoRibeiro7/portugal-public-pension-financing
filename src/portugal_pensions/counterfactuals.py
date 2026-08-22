"""Counterfactual financing utilities with explicit stock-flow consistency."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any, Literal

import pandas as pd

ContributionTiming = Literal["beginning", "mid", "end"]


def _finite(value: float, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def compound_reserve(
    contributions: Sequence[float],
    annual_returns: Sequence[float],
    *,
    initial_reserve: float = 0.0,
) -> list[float]:
    """Accumulate a hypothetical funded reserve.

    Contributions are assumed to enter at the start of each period and then earn that
    period's return. A funded-reserve counterfactual must be recorded as additional public
    expenditure unless another financing source is explicitly removed.
    """
    if len(contributions) != len(annual_returns):
        raise ValueError("contributions and annual_returns must have the same length")
    reserve = _finite(initial_reserve, "initial_reserve")
    path: list[float] = []
    for index, (contribution, annual_return) in enumerate(
        zip(contributions, annual_returns, strict=True)
    ):
        flow = _finite(contribution, f"contributions[{index}]")
        rate = _finite(annual_return, f"annual_returns[{index}]")
        if rate <= -1.0:
            raise ValueError("annual returns must be greater than -1")
        reserve = (reserve + flow) * (1.0 + rate)
        path.append(reserve)
    return path


def capitalize_cash_flows(
    cash_flows: Sequence[float],
    annual_returns: Sequence[float],
    *,
    timing: ContributionTiming,
    initial_reserve: float = 0.0,
) -> list[float]:
    """Capitalize annual cash flows under an explicit contribution-timing convention."""
    if len(cash_flows) != len(annual_returns):
        raise ValueError("cash_flows and annual_returns must have the same length")
    reserve = _finite(initial_reserve, "initial_reserve")
    path: list[float] = []
    for index, (cash_flow, annual_return) in enumerate(
        zip(cash_flows, annual_returns, strict=True)
    ):
        flow = _finite(cash_flow, f"cash_flows[{index}]")
        rate = _finite(annual_return, f"annual_returns[{index}]")
        if rate <= -1.0:
            raise ValueError("annual returns must be greater than -1")
        if timing == "beginning":
            reserve = (reserve + flow) * (1.0 + rate)
        elif timing == "mid":
            reserve = reserve * (1.0 + rate) + flow * math.sqrt(1.0 + rate)
        elif timing == "end":
            reserve = reserve * (1.0 + rate) + flow
        else:
            raise ValueError("timing must be beginning, mid, or end")
        path.append(reserve)
    return path


def funding_substitution(
    observed_state_transfer: float,
    counterfactual_employer_contribution: float,
) -> tuple[float, float]:
    """Substitute employer financing for State transfers without creating free resources.

    Returns:
        A tuple ``(employer_contribution, adjusted_state_transfer)``.
    """
    state = _finite(observed_state_transfer, "observed_state_transfer")
    employer = _finite(counterfactual_employer_contribution, "counterfactual_employer_contribution")
    adjusted_state = max(0.0, state - employer)
    effective_employer = min(employer, state)
    return effective_employer, adjusted_state


def public_worker_reallocation_flow(
    contribution_base: float,
    worker_rate: float,
    employer_rate: float,
) -> tuple[float, float, float]:
    """Compute the mechanical RGSS contribution flow for a post-2006 public cohort."""
    base = _finite(contribution_base, "contribution_base")
    worker = _finite(worker_rate, "worker_rate")
    employer = _finite(employer_rate, "employer_rate")
    if base < 0.0:
        raise ValueError("contribution_base must be non-negative")
    for name, rate in (("worker_rate", worker), ("employer_rate", employer)):
        if rate < 0.0 or rate > 1.0:
            raise ValueError(f"{name} must be between 0 and 1")
    employee_contributions = base * worker
    employer_contributions = base * employer
    return (
        employee_contributions,
        employer_contributions,
        employee_contributions + employer_contributions,
    )


def validate_counterfactual_financing_regimes(
    registry_path: str,
    regimes_path: str,
) -> list[str]:
    """Return validation errors for preregistered counterfactual regime rules."""
    registry = pd.read_csv(registry_path, dtype=str)
    regimes = pd.read_csv(regimes_path, dtype=str)
    required_registry_columns = {
        "scenario_id",
        "name",
        "description",
        "legal_or_economic",
        "assumptions",
        "status",
    }
    required_regime_columns = {
        "scenario_id",
        "scenario_name",
        "component",
        "year_start",
        "year_end",
        "perimeter",
        "stock_flow_treatment",
        "financing_source_adjustment",
        "required_input_dataset",
        "implemented_function",
        "value",
        "unit",
        "source_ids",
        "status",
        "notes",
    }
    errors = [
        *_missing_columns(registry, required_registry_columns, "counterfactual registry"),
        *_missing_columns(regimes, required_regime_columns, "counterfactual financing regimes"),
    ]
    if errors:
        return errors

    registered_ids = set(registry["scenario_id"].astype(str))
    implemented_ids = set(regimes["scenario_id"].astype(str))
    for scenario_id in sorted(registered_ids.difference(implemented_ids)):
        errors.append(f"Registered counterfactual scenario is missing from regimes: {scenario_id}")
    for scenario_id in sorted(implemented_ids.difference(registered_ids)):
        errors.append(f"Unregistered counterfactual scenario in regimes: {scenario_id}")

    duplicates = regimes[regimes.duplicated(subset=["scenario_id", "component"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate counterfactual regime row: "
            f"{_field(duplicate_row, 'scenario_id')} {_field(duplicate_row, 'component')}"
        )

    allowed_units = {"EUR_million", "not_applicable"}
    allowed_status_prefixes = (
        "blocked",
        "rule_implemented_requires_inputs",
        "complete",
        "partial",
    )
    implemented_functions = {
        "not_applicable",
        "funding_substitution",
        "compound_reserve",
        "present_value",
    }
    for row_number, record in enumerate(regimes.to_dict("records"), start=2):
        for column in required_regime_columns.difference({"value"}):
            if not _field(record, column):
                errors.append(f"Missing {column} on counterfactual regime row {row_number}")

        unit = _field(record, "unit")
        if unit and unit not in allowed_units:
            errors.append(f"Unexpected unit on counterfactual regime row {row_number}: {unit}")

        implemented_function = _field(record, "implemented_function")
        if implemented_function and implemented_function not in implemented_functions:
            errors.append(
                f"Unexpected implemented_function on counterfactual regime row {row_number}: "
                f"{implemented_function}"
            )

        status = _field(record, "status")
        if status and not status.startswith(allowed_status_prefixes):
            errors.append(f"Unexpected counterfactual regime status on row {row_number}: {status}")

        value = _field(record, "value")
        if value:
            _finite(float(value), "value")
        elif status == "complete":
            errors.append(f"Complete counterfactual regime row {row_number} missing value")

    by_id = {record["scenario_id"]: record for record in regimes.to_dict("records")}
    if "CF2" in by_id:
        adjustment = _field(by_id["CF2"], "financing_source_adjustment").lower().replace("_", "-")
        if "substitutes-one-for-one" not in adjustment:
            errors.append("CF2 must preserve one-for-one financing substitution")
    if "CF3" in by_id:
        treatment = (
            _field(by_id["CF3"], "stock_flow_treatment")
            + " "
            + _field(by_id["CF3"], "financing_source_adjustment")
            + " "
            + _field(by_id["CF3"], "notes")
        ).lower()
        if "additional" not in treatment or "expenditure" not in treatment:
            errors.append("CF3 must record funded-reserve contributions as additional expenditure")
    if "CF4" in by_id:
        bank_notes = (
            _field(by_id["CF4"], "required_input_dataset") + " " + _field(by_id["CF4"], "notes")
        ).lower()
        for required_phrase in ("cash-flow", "assets", "investment income", "state financing"):
            if required_phrase not in bank_notes:
                errors.append(f"CF4 must require {required_phrase}")

    return errors


def validate_counterfactual_execution_requirements(path: str) -> list[str]:
    """Return validation errors for counterfactual execution prerequisites."""
    requirements = pd.read_csv(path, dtype=str)
    required_columns = {
        "requirement_id",
        "scenario_id",
        "execution_step",
        "required_inputs",
        "available_inputs",
        "permitted_output",
        "status",
        "blocking_issue",
        "notes",
    }
    errors = _missing_columns(
        requirements,
        required_columns,
        "counterfactual execution requirements",
    )
    if errors:
        return errors

    duplicates = requirements[requirements.duplicated(subset=["requirement_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate counterfactual execution requirement_id: "
            f"{_field(duplicate_row, 'requirement_id')}"
        )

    required_steps = {
        ("CF1", "legal_compliance_cash_identity"),
        ("CF2", "funding_substitution_offset"),
        ("CF3", "funded_reserve_budget_cost"),
        ("CF3", "reserve_stock_flow_consistency"),
        ("CF4", "bank_lifecycle_comparison"),
        ("ALL", "stock_flow_matrix_bridge"),
        ("ALL", "numeric_output_boundary"),
    }
    allowed_statuses = {
        "blocked_missing_ledger_components",
        "rule_implemented_requires_inputs",
        "blocked_missing_contribution_and_return_series",
        "blocked_missing_cash_flow_schedule",
        "blocked_missing_system_rows",
        "bounded_claim_boundary",
    }

    observed_steps: set[tuple[str, str]] = set()
    for row_number, record in enumerate(requirements.to_dict("records"), start=2):
        for column in required_columns:
            if not _field(record, column):
                errors.append(f"Missing {column} on counterfactual execution row {row_number}")

        scenario_id = _field(record, "scenario_id")
        execution_step = _field(record, "execution_step")
        observed_steps.add((scenario_id, execution_step))
        if (scenario_id, execution_step) not in required_steps:
            errors.append(
                "Unexpected counterfactual execution requirement on row "
                f"{row_number}: {scenario_id} {execution_step}"
            )

        status = _field(record, "status")
        if status not in allowed_statuses:
            errors.append(f"Unexpected counterfactual execution status on row {row_number}")

        required_inputs = _field(record, "required_inputs").lower()
        available_inputs = _field(record, "available_inputs")
        permitted_output = _field(record, "permitted_output")
        blocking_issue = _field(record, "blocking_issue").lower()
        notes = _field(record, "notes").lower()

        if execution_step == "legal_compliance_cash_identity":
            for token in ("legal contribution", "state transfer", "pension payments"):
                if token not in required_inputs:
                    errors.append(f"CF1 execution requirement must include {token}")
            if status != "blocked_missing_ledger_components":
                errors.append("CF1 legal-compliance execution must remain blocked")
        if execution_step == "funding_substitution_offset":
            if "funding_substitution" not in available_inputs:
                errors.append("CF2 execution requirement must preserve implemented helper")
            if "one-for-one" not in available_inputs and "one-for-one" not in notes:
                errors.append("CF2 execution requirement must preserve one-for-one offset")
            if status != "rule_implemented_requires_inputs":
                errors.append("CF2 execution requirement must remain input-gated")
        if execution_step == "funded_reserve_budget_cost":
            if status != "blocked_missing_contribution_and_return_series":
                errors.append("CF3 funded-reserve budget-cost execution must remain blocked")
            if "additional historical expenditure" not in notes:
                errors.append("CF3 funded-reserve execution must preserve expenditure treatment")
            if "no_free_reserve_accumulation" not in permitted_output:
                errors.append("CF3 funded-reserve execution must block free reserve accumulation")
        if execution_step == "reserve_stock_flow_consistency":
            if "compound_reserve" not in available_inputs:
                errors.append("CF3 reserve stock-flow execution must preserve helper")
            if "annual flow costs" not in notes:
                errors.append("CF3 reserve stock-flow execution must require matching flow costs")
        if execution_step == "bank_lifecycle_comparison":
            for token in ("assets", "investment income", "state financing", "pension expenditure"):
                if token not in required_inputs:
                    errors.append(f"CF4 execution requirement must include {token}")
            if status != "blocked_missing_cash_flow_schedule":
                errors.append("CF4 bank lifecycle execution must remain blocked")
            if "no_asset_exhaustion_only_comparison" not in permitted_output:
                errors.append("CF4 execution must block asset-exhaustion-only comparison")
        if execution_step == "stock_flow_matrix_bridge":
            if "flow_of_funds_bridge_selection_requirements" not in available_inputs:
                errors.append(
                    "Counterfactual stock-flow bridge must cite flow-of-funds selection gate"
                )
            if "matrix_rows" not in permitted_output:
                errors.append("Counterfactual stock-flow bridge must require matrix rows")
        if execution_step == "numeric_output_boundary":
            if status != "bounded_claim_boundary":
                errors.append("Counterfactual numeric-output boundary must remain bounded")
            if "no_numeric_counterfactual_claim" not in permitted_output:
                errors.append("Counterfactual numeric-output boundary must block numeric claims")

        if status.startswith("blocked") and "primary" not in blocking_issue:
            errors.append(
                "Blocked counterfactual execution rows must name missing primary inputs "
                f"on row {row_number}"
            )

    for scenario_id, execution_step in required_steps.difference(observed_steps):
        errors.append(
            f"Missing counterfactual execution requirement: {scenario_id} {execution_step}"
        )

    return errors


def validate_public_worker_reallocation(
    cohort_path: str,
    contribution_path: str,
) -> list[str]:
    """Return validation errors for post-2006 public-worker reallocation files."""
    cohorts = pd.read_csv(cohort_path, dtype=str)
    contributions = pd.read_csv(contribution_path, dtype=str)
    errors = [
        *_validate_reallocation_table(
            cohorts,
            required_columns={
                "year",
                "cohort",
                "lower",
                "central",
                "upper",
                "unit",
                "source_ids",
                "status",
                "notes",
            },
            table_name="public worker cohort",
            value_columns={"lower", "central", "upper"},
            duplicate_columns=["year", "cohort"],
        ),
        *_validate_reallocation_table(
            contributions,
            required_columns={
                "year",
                "employee_contributions_lower",
                "employee_contributions_central",
                "employee_contributions_upper",
                "employer_contributions_lower",
                "employer_contributions_central",
                "employer_contributions_upper",
                "aggregate_rgss_contributions",
                "unit",
                "aggregate_unit",
                "source_ids",
                "observation_type",
                "estimation_method",
                "pension_related_basis",
                "uncertainty_basis",
                "aggregate_cap_status",
                "status",
                "missing_inputs",
                "claim_permitted",
                "notes",
            },
            table_name="public worker contribution",
            value_columns={
                "employee_contributions_lower",
                "employee_contributions_central",
                "employee_contributions_upper",
                "employer_contributions_lower",
                "employer_contributions_central",
                "employer_contributions_upper",
                "aggregate_rgss_contributions",
            },
            duplicate_columns=["year"],
        ),
        *_validate_public_worker_contribution_rules(contributions),
    ]
    for table_name, table in (
        ("public worker cohort", cohorts),
        ("public worker contribution", contributions),
    ):
        years = sorted(int(_field(record, "year")) for record in table.to_dict("records"))
        if years != list(range(2006, 2026)):
            errors.append(f"{table_name} table must cover every year from 2006 to 2025")
    return errors


def _validate_public_worker_contribution_rules(contributions: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    if _missing_columns(
        contributions,
        {
            "employee_contributions_lower",
            "employee_contributions_central",
            "employee_contributions_upper",
            "employer_contributions_lower",
            "employer_contributions_central",
            "employer_contributions_upper",
            "aggregate_rgss_contributions",
            "estimation_method",
            "pension_related_basis",
            "uncertainty_basis",
            "aggregate_cap_status",
            "status",
            "missing_inputs",
            "claim_permitted",
        },
        "public worker contribution",
    ):
        return errors

    for row_number, record in enumerate(contributions.to_dict("records"), start=2):
        status = _field(record, "status")
        method = _field(record, "estimation_method")
        cap_status = _field(record, "aggregate_cap_status")
        pension_basis = _field(record, "pension_related_basis")
        if status.startswith("blocked"):
            if method != "blocked_source_gap":
                errors.append(
                    "Blocked public worker contribution rows must use blocked_source_gap "
                    f"on row {row_number}"
                )
            if _field(record, "claim_permitted") != "no":
                errors.append(
                    "Blocked public worker contribution rows must not permit claims "
                    f"on row {row_number}"
                )
            missing_inputs = {
                value.strip()
                for value in _field(record, "missing_inputs").split(";")
                if value.strip()
            }
            for required_input in (
                "public_worker_new_entrant_counts",
                "contribution_base_payroll",
                "applicable_rgss_worker_rate",
                "applicable_rgss_employer_rate",
                "aggregate_rgss_contribution_revenue",
            ):
                if required_input not in missing_inputs:
                    errors.append(
                        "Blocked public worker contribution row is missing required "
                        f"input blocker {required_input} on row {row_number}"
                    )
        else:
            if method not in {"direct_observation", "reconstruction"}:
                errors.append(
                    "Estimated public worker contribution rows must identify direct "
                    f"observation or reconstruction on row {row_number}"
                )
            if pension_basis in {"", "blocked_not_decomposed"}:
                errors.append(
                    "Estimated public worker contribution rows must state pension-related "
                    f"basis on row {row_number}"
                )
            if not _field(record, "uncertainty_basis"):
                errors.append(
                    "Estimated public worker contribution rows must state uncertainty basis "
                    f"on row {row_number}"
                )
            if cap_status != "checked_against_aggregate_rgss_revenue":
                errors.append(
                    "Estimated public worker contribution rows must be checked against "
                    f"aggregate RGSS revenue on row {row_number}"
                )

        employee_bounds = _bounds(record, "employee_contributions")
        employer_bounds = _bounds(record, "employer_contributions")
        for label, bounds in (("employee", employee_bounds), ("employer", employer_bounds)):
            if bounds is not None:
                lower, central, upper = bounds
                if lower > central or central > upper:
                    errors.append(
                        f"{label} contribution bounds must satisfy lower <= central <= upper "
                        f"on row {row_number}"
                    )

        aggregate = _optional_float(record, "aggregate_rgss_contributions")
        central_total = _central_total(record)
        if aggregate is not None and central_total is not None and central_total > aggregate + 0.01:
            errors.append(
                "Public worker contribution estimate exceeds aggregate RGSS revenue "
                f"on row {row_number}"
            )
    return errors


def validate_public_worker_reallocation_bridge(
    bridge_path: str,
    source_registry_path: str | None = None,
) -> list[str]:
    """Return validation errors for the post-2006 public-worker flow bridge."""
    bridge = pd.read_csv(bridge_path, dtype=str, keep_default_na=False)
    required_columns = {
        "year",
        "mechanism",
        "flow_component",
        "worker_count",
        "contribution_base",
        "worker_rate",
        "employer_rate",
        "employee_contributions",
        "employer_contributions",
        "total_contributions",
        "unit",
        "price_basis",
        "accounting_basis",
        "excluded_effects",
        "source_ids",
        "status",
        "missing_inputs",
        "claim_permitted",
        "notes",
    }
    value_columns = {
        "worker_count",
        "contribution_base",
        "worker_rate",
        "employer_rate",
        "employee_contributions",
        "employer_contributions",
        "total_contributions",
    }
    errors = _missing_columns(bridge, required_columns, "public worker reallocation bridge")
    if errors:
        return errors

    duplicates = bridge[
        bridge.duplicated(subset=["year", "mechanism", "flow_component"], keep=False)
    ]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate public worker reallocation bridge row for "
            f"year {_field(duplicate_row, 'year')}"
        )

    years: list[int] = []
    source_ids = _registered_source_ids(source_registry_path)
    required_missing_inputs = {
        "public_worker_new_entrant_counts",
        "contribution_base_payroll",
        "applicable_rgss_worker_rate",
        "applicable_rgss_employer_rate",
    }
    excluded_effects = {
        "demographic_change",
        "wage_growth",
        "general_labour_market_effects",
    }

    for row_number, record in enumerate(bridge.to_dict("records"), start=2):
        year_text = _field(record, "year")
        try:
            years.append(int(year_text))
        except ValueError:
            errors.append(f"Invalid year on public worker reallocation bridge row {row_number}")

        for column in required_columns.difference(value_columns):
            if not _field(record, column):
                errors.append(
                    f"Missing {column} on public worker reallocation bridge row {row_number}"
                )
        if _field(record, "mechanism") != "post_2006_cga_closure_new_entrants_to_rgss":
            errors.append(
                f"Unexpected mechanism on public worker reallocation bridge row {row_number}"
            )
        if _field(record, "flow_component") != "mechanical_reallocation":
            errors.append(
                "public worker reallocation bridge must isolate mechanical_reallocation "
                f"on row {row_number}"
            )
        observed_exclusions = {
            value.strip()
            for value in _field(record, "excluded_effects").split(";")
            if value.strip()
        }
        if not excluded_effects.issubset(observed_exclusions):
            errors.append(
                "public worker reallocation bridge must exclude demographic wage and "
                f"labour-market effects on row {row_number}"
            )

        status = _field(record, "status")
        if not (status.startswith("blocked") or status in {"estimated", "complete"}):
            errors.append(
                f"Unexpected public worker reallocation bridge status on row {row_number}: {status}"
            )
        missing_inputs = {
            value.strip() for value in _field(record, "missing_inputs").split(";") if value.strip()
        }
        if status.startswith("blocked"):
            if _field(record, "claim_permitted") != "no":
                errors.append(
                    "Blocked public worker reallocation bridge rows must not permit claims "
                    f"on row {row_number}"
                )
            if not required_missing_inputs.issubset(missing_inputs):
                errors.append(
                    "Blocked public worker reallocation bridge row is missing required "
                    f"input blockers on row {row_number}"
                )

        numeric_values: dict[str, float] = {}
        for column in value_columns:
            value = _field(record, column)
            if not value:
                continue
            try:
                numeric_value = _finite(float(value), column)
            except ValueError:
                errors.append(
                    f"{column} must be numeric on public worker reallocation bridge row "
                    f"{row_number}"
                )
                continue
            if numeric_value < 0.0:
                errors.append(
                    f"{column} must be non-negative on public worker reallocation bridge "
                    f"row {row_number}"
                )
            if column in {"worker_rate", "employer_rate"} and numeric_value > 1.0:
                errors.append(
                    f"{column} must be at most 1 on public worker reallocation bridge "
                    f"row {row_number}"
                )
            numeric_values[column] = numeric_value

        if status == "complete":
            missing_numeric = sorted(value_columns.difference(numeric_values))
            for column in missing_numeric:
                errors.append(
                    f"Missing {column} on complete public worker reallocation bridge row "
                    f"{row_number}"
                )
        formula_columns = {
            "contribution_base",
            "worker_rate",
            "employer_rate",
            "employee_contributions",
            "employer_contributions",
            "total_contributions",
        }
        if formula_columns.issubset(numeric_values):
            try:
                employee, employer, total = public_worker_reallocation_flow(
                    numeric_values["contribution_base"],
                    numeric_values["worker_rate"],
                    numeric_values["employer_rate"],
                )
            except ValueError as error:
                errors.append(
                    "Invalid contribution-flow inputs on public worker reallocation bridge "
                    f"row {row_number}: {error}"
                )
                continue
            if not math.isclose(
                numeric_values["employee_contributions"], employee, rel_tol=0.0, abs_tol=0.01
            ):
                errors.append(
                    "Employee contribution residual on public worker reallocation bridge "
                    f"row {row_number}"
                )
            if not math.isclose(
                numeric_values["employer_contributions"], employer, rel_tol=0.0, abs_tol=0.01
            ):
                errors.append(
                    "Employer contribution residual on public worker reallocation bridge "
                    f"row {row_number}"
                )
            if not math.isclose(
                numeric_values["total_contributions"], total, rel_tol=0.0, abs_tol=0.01
            ):
                errors.append(
                    "Total contribution residual on public worker reallocation bridge "
                    f"row {row_number}"
                )

        for source_id in _field(record, "source_ids").split(";"):
            source_id = source_id.strip()
            if source_ids is not None and source_id and source_id not in source_ids:
                errors.append(
                    f"Unknown source_id on public worker reallocation bridge row "
                    f"{row_number}: {source_id}"
                )

    if sorted(years) != list(range(2006, 2026)):
        errors.append("public worker reallocation bridge must cover every year from 2006 to 2025")
    return errors


def validate_public_worker_liability_assumptions(
    assumptions_path: str,
    source_registry_path: str | None = None,
) -> list[str]:
    """Return validation errors for public-worker future-rights assumption gates."""
    assumptions = pd.read_csv(assumptions_path, dtype=str, keep_default_na=False)
    required_columns = {
        "assumption_id",
        "scope",
        "period_start",
        "period_end",
        "current_flow_dataset",
        "rights_measure",
        "liability_measurement_basis",
        "discount_rate_basis",
        "mortality_basis",
        "indexation_basis",
        "microdata_status",
        "aggregate_bounds_status",
        "required_inputs",
        "source_ids",
        "status",
        "claim_constraint",
        "notes",
    }
    errors = _missing_columns(assumptions, required_columns, "public worker liability assumptions")
    if errors:
        return errors

    duplicates = assumptions[assumptions.duplicated(subset=["assumption_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate public worker liability assumption_id: "
            f"{_field(duplicate_row, 'assumption_id')}"
        )

    source_ids = _registered_source_ids(source_registry_path)
    has_flow_rights_gate = False
    required_inputs = {
        "cohort_counts",
        "contribution_bases",
        "service_histories",
        "benefit_formula",
        "indexation_rule",
        "mortality_table",
        "discount_rate",
    }
    for row_number, record in enumerate(assumptions.to_dict("records"), start=2):
        for column in required_columns:
            if not _field(record, column):
                errors.append(
                    f"Missing {column} on public worker liability assumption row {row_number}"
                )
        try:
            period_start = int(_field(record, "period_start"))
            period_end = int(_field(record, "period_end"))
        except ValueError:
            errors.append(f"Invalid period on public worker liability assumption row {row_number}")
            continue
        if period_start > period_end:
            errors.append(
                "public worker liability assumption period_start must be <= period_end "
                f"on row {row_number}"
            )
        if period_start <= 2006 and period_end >= 2025:
            has_flow_rights_gate = True

        if _field(record, "current_flow_dataset") != (
            "data/processed/public_worker_rgss_contributions_2006_2025.csv"
        ):
            errors.append(
                "public worker liability assumptions must reference the contribution "
                f"dataset on row {row_number}"
            )
        claim_constraint = _field(record, "claim_constraint").lower()
        if "free" not in claim_constraint or "pension rights" not in claim_constraint:
            errors.append(
                "public worker liability assumptions must block free-sustainability "
                f"claims without pension-rights caveats on row {row_number}"
            )
        observed_inputs = {
            value.strip() for value in _field(record, "required_inputs").split(";") if value.strip()
        }
        if not required_inputs.issubset(observed_inputs):
            errors.append(
                "public worker liability assumption row is missing required actuarial "
                f"inputs on row {row_number}"
            )
        if not _field(record, "status").startswith("blocked"):
            if _field(record, "microdata_status").startswith("missing"):
                errors.append(
                    "non-blocked public worker liability assumptions require microdata "
                    f"or documented aggregate bounds on row {row_number}"
                )
            if _field(record, "aggregate_bounds_status").startswith("missing"):
                errors.append(
                    "non-blocked public worker liability assumptions require aggregate "
                    f"bounds on row {row_number}"
                )
        for source_id in _field(record, "source_ids").split(";"):
            source_id = source_id.strip()
            if source_ids is not None and source_id and source_id not in source_ids:
                errors.append(
                    f"Unknown source_id on public worker liability assumption row "
                    f"{row_number}: {source_id}"
                )

    if not has_flow_rights_gate:
        errors.append(
            "public worker liability assumptions must cover the full 2006-2025 flow period"
        )
    return errors


def validate_fefss_return_inputs(
    returns_path: str,
    capitalization_path: str,
    source_registry_path: str | None = None,
    sensitivity_path: str | None = None,
) -> list[str]:
    """Return validation errors for FEFSS return and capitalization inputs."""
    returns = pd.read_csv(returns_path, dtype=str, keep_default_na=False)
    capitalization = pd.read_csv(capitalization_path, dtype=str, keep_default_na=False)
    errors = [
        *_validate_fefss_returns(returns, source_registry_path),
        *_validate_fefss_capitalization(capitalization, source_registry_path),
    ]
    if sensitivity_path is not None:
        sensitivity = pd.read_csv(sensitivity_path, dtype=str, keep_default_na=False)
        errors.extend(_validate_fefss_sensitivity(sensitivity, source_registry_path))
    return errors


def _validate_fefss_returns(
    returns: pd.DataFrame,
    source_registry_path: str | None,
) -> list[str]:
    required_columns = {
        "year",
        "reported_return",
        "return_type",
        "valuation_basis",
        "fees_basis",
        "nominal_real_basis",
        "source_ids",
        "page",
        "status",
        "missing_inputs",
        "notes",
    }
    errors = _missing_columns(returns, required_columns, "FEFSS returns")
    if errors:
        return errors
    source_ids = _registered_source_ids(source_registry_path)
    duplicates = returns[returns.duplicated(subset=["year"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(f"Duplicate FEFSS return row for year {_field(duplicate_row, 'year')}")
    years: list[int] = []
    for row_number, record in enumerate(returns.to_dict("records"), start=2):
        try:
            years.append(int(_field(record, "year")))
        except ValueError:
            errors.append(f"Invalid year on FEFSS return row {row_number}")
        status = _field(record, "status")
        if not (status.startswith("blocked") or status in {"observed", "complete"}):
            errors.append(f"Unexpected FEFSS return status on row {row_number}: {status}")
        if status.startswith("blocked"):
            if _field(record, "reported_return"):
                errors.append(
                    f"Blocked FEFSS return row must not contain a return on row {row_number}"
                )
            missing_inputs = {
                value.strip()
                for value in _field(record, "missing_inputs").split(";")
                if value.strip()
            }
            for required_input in (
                "official_annual_return",
                "return_type",
                "valuation_basis",
                "fees_basis",
            ):
                if required_input not in missing_inputs:
                    errors.append(
                        f"Blocked FEFSS return row missing {required_input} on row {row_number}"
                    )
        else:
            for column in {
                "reported_return",
                "return_type",
                "valuation_basis",
                "fees_basis",
                "nominal_real_basis",
                "page",
            }:
                if not _field(record, column):
                    errors.append(f"Missing {column} on observed FEFSS return row {row_number}")
            return_value = _optional_float(record, "reported_return")
            if return_value is not None and return_value <= -1.0:
                errors.append(f"FEFSS reported_return must be greater than -1 on row {row_number}")
        for source_id in _field(record, "source_ids").split(";"):
            source_id = source_id.strip()
            if source_ids is not None and source_id and source_id not in source_ids:
                errors.append(f"Unknown source_id on FEFSS return row {row_number}: {source_id}")
    if sorted(years) != list(range(2006, 2026)):
        errors.append("FEFSS returns must cover every year from 2006 to 2025")
    return errors


def _validate_fefss_capitalization(
    capitalization: pd.DataFrame,
    source_registry_path: str | None,
) -> list[str]:
    required_columns = {
        "scenario_id",
        "year",
        "cash_flow",
        "timing",
        "annual_return",
        "reserve_value",
        "actual_fefss_assets",
        "comparison_ratio",
        "unit",
        "price_basis",
        "nominal_real_basis",
        "return_source",
        "benchmark_source",
        "financing_assumption",
        "retained_resources_required",
        "offsetting_financing_assumption",
        "source_ids",
        "status",
        "missing_inputs",
        "claim_permitted",
        "notes",
    }
    errors = _missing_columns(capitalization, required_columns, "FEFSS capitalization")
    if errors:
        return errors
    source_ids = _registered_source_ids(source_registry_path)
    required_timings = {"beginning", "mid", "end"}
    observed_timings = set(capitalization["timing"].dropna().astype(str))
    if not required_timings.issubset(observed_timings):
        errors.append("FEFSS capitalization must include beginning mid and end timing rows")
    duplicates = capitalization[
        capitalization.duplicated(subset=["scenario_id", "year", "timing"], keep=False)
    ]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate FEFSS capitalization row for "
            f"{_field(duplicate_row, 'scenario_id')} "
            f"{_field(duplicate_row, 'year')} {_field(duplicate_row, 'timing')}"
        )
    for row_number, record in enumerate(capitalization.to_dict("records"), start=2):
        for column in required_columns.difference(
            {
                "cash_flow",
                "annual_return",
                "reserve_value",
                "actual_fefss_assets",
                "comparison_ratio",
                "offsetting_financing_assumption",
                "missing_inputs",
            }
        ):
            if not _field(record, column):
                errors.append(f"Missing {column} on FEFSS capitalization row {row_number}")
        timing = _field(record, "timing")
        if timing not in required_timings:
            errors.append(f"Unexpected FEFSS capitalization timing on row {row_number}: {timing}")
        status = _field(record, "status")
        if not (status.startswith("blocked") or status in {"estimated", "complete"}):
            errors.append(f"Unexpected FEFSS capitalization status on row {row_number}: {status}")
        missing_inputs = {
            value.strip() for value in _field(record, "missing_inputs").split(";") if value.strip()
        }
        if status.startswith("blocked"):
            for required_input in {"cash_flow", "annual_return"}:
                if required_input not in missing_inputs:
                    errors.append(
                        "Blocked FEFSS capitalization row missing "
                        f"{required_input} on row {row_number}"
                    )
            if _field(record, "claim_permitted") != "no":
                errors.append(
                    f"Blocked FEFSS capitalization rows must not permit claims on row {row_number}"
                )
        if _field(record, "retained_resources_required") != "yes" and not _field(
            record, "offsetting_financing_assumption"
        ):
            errors.append(
                "FEFSS capitalization rows must require retained resources unless an "
                f"offsetting financing assumption is specified on row {row_number}"
            )
        if _field(record, "return_source") == _field(record, "benchmark_source"):
            errors.append(
                "FEFSS capitalization rows must distinguish return source from benchmark "
                f"source on row {row_number}"
            )
        for column in {
            "cash_flow",
            "annual_return",
            "reserve_value",
            "actual_fefss_assets",
            "comparison_ratio",
        }:
            value = _field(record, column)
            if value:
                _finite(float(value), column)
        annual_return = _optional_float(record, "annual_return")
        if annual_return is not None and annual_return <= -1.0:
            errors.append(f"FEFSS annual_return must be greater than -1 on row {row_number}")
        for source_id in _field(record, "source_ids").split(";"):
            source_id = source_id.strip()
            if source_ids is not None and source_id and source_id not in source_ids:
                errors.append(
                    f"Unknown source_id on FEFSS capitalization row {row_number}: {source_id}"
                )
    return errors


def _validate_fefss_sensitivity(
    sensitivity: pd.DataFrame,
    source_registry_path: str | None,
) -> list[str]:
    required_columns = {
        "scenario_id",
        "benchmark",
        "return_basis",
        "timing",
        "year_start",
        "year_end",
        "cash_flow_source",
        "return_source",
        "financing_assumption",
        "retained_resources_required",
        "offsetting_financing_assumption",
        "nominal_value",
        "real_value",
        "actual_fefss_assets",
        "unit",
        "source_ids",
        "status",
        "missing_inputs",
        "claim_permitted",
        "notes",
    }
    errors = _missing_columns(sensitivity, required_columns, "FEFSS sensitivity")
    if errors:
        return errors
    source_ids = _registered_source_ids(source_registry_path)
    required_benchmarks = {
        "fefss_observed_returns",
        "low_risk_government_financing",
        "actual_fefss_assets_reference",
    }
    observed_benchmarks = set(sensitivity["benchmark"].dropna().astype(str))
    if not required_benchmarks.issubset(observed_benchmarks):
        errors.append(
            "FEFSS sensitivity must include observed returns low-risk benchmark and actual assets"
        )
    for row_number, record in enumerate(sensitivity.to_dict("records"), start=2):
        for column in required_columns.difference(
            {
                "offsetting_financing_assumption",
                "nominal_value",
                "real_value",
                "actual_fefss_assets",
            }
        ):
            if not _field(record, column):
                errors.append(f"Missing {column} on FEFSS sensitivity row {row_number}")
        try:
            year_start = int(_field(record, "year_start"))
            year_end = int(_field(record, "year_end"))
        except ValueError:
            errors.append(f"Invalid year range on FEFSS sensitivity row {row_number}")
            continue
        if year_start > year_end:
            errors.append(f"FEFSS sensitivity year_start must be <= year_end on row {row_number}")
        if year_start > 2006 or year_end < 2025:
            errors.append(f"FEFSS sensitivity rows must cover 2006-2025 on row {row_number}")
        if _field(record, "timing") not in {"beginning", "mid", "end", "not_applicable"}:
            errors.append(f"Unexpected FEFSS sensitivity timing on row {row_number}")
        status = _field(record, "status")
        if not (status.startswith("blocked") or status in {"estimated", "complete"}):
            errors.append(f"Unexpected FEFSS sensitivity status on row {row_number}: {status}")
        if status.startswith("blocked") and _field(record, "claim_permitted") != "no":
            errors.append(
                f"Blocked FEFSS sensitivity rows must not permit claims on row {row_number}"
            )
        if _field(record, "retained_resources_required") != "yes" and not _field(
            record, "offsetting_financing_assumption"
        ):
            errors.append(
                "FEFSS sensitivity rows must require retained resources unless an "
                f"offsetting financing assumption is specified on row {row_number}"
            )
        for column in {"nominal_value", "real_value", "actual_fefss_assets"}:
            value = _field(record, column)
            if value:
                _finite(float(value), column)
        for source_id in _field(record, "source_ids").split(";"):
            source_id = source_id.strip()
            if source_ids is not None and source_id and source_id not in source_ids:
                errors.append(
                    f"Unknown source_id on FEFSS sensitivity row {row_number}: {source_id}"
                )
    return errors


def _missing_columns(
    table: pd.DataFrame,
    required_columns: set[str],
    table_name: str,
) -> list[str]:
    missing_columns = sorted(required_columns.difference(table.columns))
    if missing_columns:
        return [f"{table_name} missing columns: {', '.join(missing_columns)}"]
    return []


def _validate_reallocation_table(
    table: pd.DataFrame,
    *,
    required_columns: set[str],
    table_name: str,
    value_columns: set[str],
    duplicate_columns: list[str],
) -> list[str]:
    missing_columns = sorted(required_columns.difference(table.columns))
    if missing_columns:
        return [f"{table_name} table missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = table[table.duplicated(subset=duplicate_columns, keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(f"Duplicate {table_name} row for year {_field(duplicate_row, 'year')}")

    for row_number, record in enumerate(table.to_dict("records"), start=2):
        for column in required_columns.difference(value_columns):
            if not _field(record, column):
                errors.append(f"Missing {column} on {table_name} row {row_number}")
        status = _field(record, "status")
        if not (status.startswith("blocked") or status in {"estimated", "complete"}):
            errors.append(f"Unexpected {table_name} status on row {row_number}: {status}")
        for column in value_columns:
            value = _field(record, column)
            if value and _finite(float(value), column) < 0.0:
                errors.append(f"{column} must be non-negative on {table_name} row {row_number}")
    return errors


def _field(row: Any, column: str) -> str:
    value = row[column]
    if pd.isna(value):
        return ""
    return str(value).strip()


def _optional_float(row: Any, column: str) -> float | None:
    value = _field(row, column)
    if not value:
        return None
    return _finite(float(value), column)


def _bounds(row: Any, prefix: str) -> tuple[float, float, float] | None:
    values = tuple(
        _optional_float(row, f"{prefix}_{suffix}") for suffix in ("lower", "central", "upper")
    )
    if any(value is None for value in values):
        return None
    lower, central, upper = values
    assert lower is not None
    assert central is not None
    assert upper is not None
    return lower, central, upper


def _central_total(row: Any) -> float | None:
    employee = _optional_float(row, "employee_contributions_central")
    employer = _optional_float(row, "employer_contributions_central")
    if employee is None or employer is None:
        return None
    return employee + employer


def _registered_source_ids(source_registry_path: str | None) -> set[str] | None:
    if source_registry_path is None:
        return None
    sources = pd.read_csv(source_registry_path, dtype=str, keep_default_na=False)
    if "source_id" not in sources.columns:
        return set()
    return set(sources["source_id"])
