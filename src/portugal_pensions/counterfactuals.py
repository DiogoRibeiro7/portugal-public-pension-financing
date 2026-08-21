"""Counterfactual financing utilities with explicit stock-flow consistency."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

import pandas as pd


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
                "unit",
                "source_ids",
                "observation_type",
                "status",
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
            },
            duplicate_columns=["year"],
        ),
    ]
    for table_name, table in (
        ("public worker cohort", cohorts),
        ("public worker contribution", contributions),
    ):
        years = sorted(int(_field(record, "year")) for record in table.to_dict("records"))
        if years != list(range(2006, 2026)):
            errors.append(f"{table_name} table must cover every year from 2006 to 2025")
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


def _registered_source_ids(source_registry_path: str | None) -> set[str] | None:
    if source_registry_path is None:
        return None
    sources = pd.read_csv(source_registry_path, dtype=str, keep_default_na=False)
    if "source_id" not in sources.columns:
        return set()
    return set(sources["source_id"])
