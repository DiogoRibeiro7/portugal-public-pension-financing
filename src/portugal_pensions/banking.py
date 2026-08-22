"""Banking-sector pension transfer calculations.

The module intentionally separates actuarial valuation from accounting reconciliation.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True, slots=True)
class BankTransferBalance:
    """Annual cash reconciliation for transferred banking-sector pensions."""

    expenditure: float
    financing: float
    residual_burden: float


def _finite(value: float, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    return numeric


def present_value(cash_flows: Sequence[float], annual_discount_rate: float) -> float:
    """Return the end-of-period present value of deterministic annual cash flows.

    Args:
        cash_flows: Cash flows at t=1, ..., n.
        annual_discount_rate: Annual effective discount rate. Must exceed -1.

    Returns:
        Present value at t=0.
    """
    rate = _finite(annual_discount_rate, "annual_discount_rate")
    if rate <= -1.0:
        raise ValueError("annual_discount_rate must be greater than -1")
    values: list[float] = []
    for index, cash_flow in enumerate(cash_flows, start=1):
        amount = _finite(cash_flow, f"cash_flows[{index - 1}]")
        values.append(amount / ((1.0 + rate) ** index))
    return float(sum(values))


def bank_transfer_balance(
    *,
    pension_expenditure: float,
    administrative_cost: float,
    state_specific_transfer: float,
    attributable_asset_financing: float = 0.0,
    other_financing: float = 0.0,
) -> BankTransferBalance:
    """Compute the annual residual funding burden of transferred bank pensions.

    A positive residual means pension and administrative expenditure exceeds the recorded
    financing sources supplied to this ledger. It must not automatically be interpreted as
    a loss to Social Security until timing and perimeter adjustments have been investigated.
    """
    expenditure = _finite(pension_expenditure, "pension_expenditure") + _finite(
        administrative_cost, "administrative_cost"
    )
    financing = (
        _finite(state_specific_transfer, "state_specific_transfer")
        + _finite(attributable_asset_financing, "attributable_asset_financing")
        + _finite(other_financing, "other_financing")
    )
    return BankTransferBalance(
        expenditure=expenditure,
        financing=financing,
        residual_burden=expenditure - financing,
    )


def required_assets_for_cash_flows(
    cash_flows: Sequence[float], annual_discount_rate: float
) -> float:
    """Alias with domain semantics for pension-liability sensitivity analysis."""
    return present_value(cash_flows, annual_discount_rate)


def validate_bank_pension_transfer_registry(path: str) -> list[str]:
    """Return validation errors for the bank pension-transfer legal registry."""
    registry = pd.read_csv(path, dtype=str)
    required_columns = {
        "record_id",
        "legal_source_id",
        "instrument",
        "publication_date",
        "effective_date",
        "category",
        "article",
        "subject",
        "legal_rule",
        "value",
        "unit",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(registry.columns))
    if missing_columns:
        return [f"Bank pension transfer registry missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = registry[registry.duplicated(subset=["record_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate bank transfer registry record_id: {_field(duplicate_row, 'record_id')}"
        )

    required_categories = {
        "pensions_assumed",
        "liabilities_retained_by_banks",
        "assets_transferred",
        "state_financing",
        "valuation_date",
        "legal_discount_rate",
        "mortality_table",
        "independent_valuation",
        "asset_composition_constraint",
        "transfer_schedule",
        "participating_institution",
        "extinguishment_rule",
    }
    categories = set(registry["category"].dropna().astype(str))
    for category in sorted(required_categories.difference(categories)):
        errors.append(f"Missing DL127 bank transfer category: {category}")

    institution_count = int((registry["category"].astype(str) == "participating_institution").sum())
    if institution_count != 18:
        errors.append(f"Expected 18 participating institutions, found {institution_count}")

    for row_number, record in enumerate(registry.to_dict("records"), start=2):
        for column in required_columns.difference({"value", "unit"}):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank transfer registry row {row_number}")
        status = _field(record, "status")
        if status not in {"source_acquired", "official_detail_registered"}:
            errors.append(f"Unexpected bank transfer registry status on row {row_number}: {status}")

    expected_numeric = {
        "DL127_VALUATION_2": 0.04,
        "DL127_VALUATION_6": 0.005,
        "DL127_ASSET_2": 0.50,
        "DL127_SCHEDULE_1": 0.55,
        "DL127_SCHEDULE_3": 0.95,
    }
    for record_id, expected_value in expected_numeric.items():
        matches = registry[registry["record_id"] == record_id]
        if matches.empty:
            errors.append(f"Missing bank transfer numeric row: {record_id}")
            continue
        actual = _field(matches.iloc[0], "value")
        if not actual or not math.isclose(
            float(actual), expected_value, rel_tol=0.0, abs_tol=1e-12
        ):
            errors.append(f"Unexpected value for {record_id}: {actual}")
    return errors


def validate_bank_transfer_legal_coverage(coverage_path: str, registry_path: str) -> list[str]:
    """Return validation errors for the bank-transfer legal coverage gate."""
    coverage = pd.read_csv(coverage_path, dtype=str, keep_default_na=False)
    registry = pd.read_csv(registry_path, dtype=str, keep_default_na=False)
    required_columns = {
        "coverage_id",
        "legal_source_id",
        "instrument",
        "requirement",
        "registry_record_ids",
        "coverage_status",
        "limitation",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(coverage.columns))
    if missing_columns:
        return [f"Bank transfer legal coverage missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = coverage[coverage.duplicated(subset=["coverage_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate bank transfer legal coverage_id: {_field(duplicate_row, 'coverage_id')}"
        )

    required_sources = {"DR_DL54_2009", "DR_DL1A_2011", "DR_DL127_2011", "DR_DL88_2012"}
    observed_sources = set(coverage["legal_source_id"])
    for source_id in sorted(required_sources.difference(observed_sources)):
        errors.append(f"Missing bank transfer legal source coverage: {source_id}")

    required_dl127_requirements = {
        "asset_composition_constraints",
        "assets_transferred",
        "extinguishing_covered_bank_liabilities",
        "independent_valuation_procedure",
        "legal_discount_rate",
        "liabilities_retained_by_banks",
        "mortality_tables",
        "participating_institutions",
        "pensions_assumed",
        "state_financing",
        "transfer_schedule",
        "valuation_date",
    }
    observed_dl127_requirements = set(
        coverage.loc[coverage["legal_source_id"] == "DR_DL127_2011", "requirement"]
    )
    for requirement in sorted(required_dl127_requirements.difference(observed_dl127_requirements)):
        errors.append(f"Missing DL127 legal coverage requirement: {requirement}")

    allowed_statuses = {"official_detail_registered", "source_acquired"}
    registry_ids = set(registry["record_id"])
    for row_number, record in enumerate(coverage.to_dict("records"), start=2):
        for column in required_columns:
            if not _field(record, column):
                errors.append(f"Missing {column} on bank transfer legal coverage row {row_number}")
        status = _field(record, "coverage_status")
        if status not in allowed_statuses:
            errors.append(f"Unexpected bank transfer legal coverage status on row {row_number}")
        source_id = _field(record, "legal_source_id")
        limitation = _field(record, "limitation")
        if source_id == "DR_DL127_2011" and "raw_pdf" not in limitation:
            errors.append("DL127 coverage rows must preserve the raw-PDF limitation")
        for record_id in _field(record, "registry_record_ids").split(";"):
            if record_id and record_id not in registry_ids:
                errors.append(
                    f"Bank transfer legal coverage row {row_number} references unknown registry "
                    f"record: {record_id}"
                )

    participating = coverage[coverage["requirement"].astype(str) == "participating_institutions"]
    if participating.empty:
        errors.append("Missing participating-institutions coverage row")
    else:
        institution_ids = [
            record_id
            for record_id in _field(participating.iloc[0], "registry_record_ids").split(";")
            if record_id
        ]
        if len(institution_ids) != 18:
            errors.append("Participating-institutions coverage must reference 18 registry records")
    return errors


def validate_bank_worker_rgss_contributions(
    contributions_path: str, mapping_path: str
) -> list[str]:
    """Return validation errors for bank-worker RGSS contribution-flow separation."""
    contributions = pd.read_csv(contributions_path, dtype=str, keep_default_na=False)
    mapping = pd.read_csv(mapping_path, dtype=str, keep_default_na=False)
    required_contribution_columns = {
        "record_id",
        "year",
        "population_id",
        "legal_source_ids",
        "legal_basis",
        "contingency_scope",
        "employee_contributions",
        "employer_contributions",
        "unit",
        "accounting_basis",
        "perimeter",
        "separation_from_pension_transfer",
        "reconciliation_source_ids",
        "status",
        "blocking_issue",
        "notes",
    }
    required_mapping_columns = {
        "population_id",
        "legal_source_id",
        "instrument",
        "effective_date",
        "population",
        "rgss_integration_status",
        "covered_contingencies",
        "retained_or_excluded_contingencies",
        "relationship_to_2011_pension_transfer",
        "source_registry_status",
        "contribution_flow_status",
        "notes",
    }
    missing_contribution_columns = sorted(
        required_contribution_columns.difference(contributions.columns)
    )
    if missing_contribution_columns:
        return [
            "Bank-worker RGSS contributions missing columns: "
            f"{', '.join(missing_contribution_columns)}"
        ]
    missing_mapping_columns = sorted(required_mapping_columns.difference(mapping.columns))
    if missing_mapping_columns:
        return [
            "Bank-worker legal population mapping missing columns: "
            f"{', '.join(missing_mapping_columns)}"
        ]

    errors: list[str] = []
    required_populations = {
        "active_bank_workers_cafeb_integration",
        "new_bank_workers_rgss",
        "pensioners_in_payment_dl127_excluded",
    }
    contribution_populations = set(contributions["population_id"])
    mapping_populations = set(mapping["population_id"])
    for population_id in sorted(required_populations.difference(contribution_populations)):
        errors.append(f"Missing bank-worker contribution population: {population_id}")
    for population_id in sorted(required_populations.difference(mapping_populations)):
        errors.append(f"Missing bank-worker legal population mapping: {population_id}")

    allowed_statuses = {
        "blocked_missing_official_flow_inputs",
        "not_applicable",
        "reconciled_to_official_accounts",
    }
    allowed_units = {"EUR_million", "not_applicable"}
    duplicates = contributions[contributions.duplicated(subset=["record_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate bank-worker contribution record_id: {_field(duplicate_row, 'record_id')}"
        )
    duplicate_mappings = mapping[mapping.duplicated(subset=["population_id"], keep=False)]
    for _, duplicate_row in duplicate_mappings.iterrows():
        errors.append(
            f"Duplicate bank-worker population mapping: {_field(duplicate_row, 'population_id')}"
        )

    for row_number, record in enumerate(contributions.to_dict("records"), start=2):
        for column in required_contribution_columns.difference(
            {"employee_contributions", "employer_contributions"}
        ):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank-worker contribution row {row_number}")
        if _field(record, "unit") not in allowed_units:
            errors.append(f"Unexpected bank-worker contribution unit on row {row_number}")
        status = _field(record, "status")
        if status not in allowed_statuses:
            errors.append(f"Unexpected bank-worker contribution status on row {row_number}")
        if _field(record, "population_id") not in mapping_populations:
            errors.append(
                f"Bank-worker contribution row {row_number} references unknown population"
            )
        if "pension_fund_assets" not in _field(record, "separation_from_pension_transfer"):
            errors.append(
                "Bank-worker contribution rows must state they are not pension-fund assets "
                f"on row {row_number}"
            )
        if status == "blocked_missing_official_flow_inputs":
            if _field(record, "employee_contributions") or _field(record, "employer_contributions"):
                errors.append(
                    "Blocked bank-worker contribution rows must not contain contribution values "
                    f"on row {row_number}"
                )
            if "primary" not in _field(record, "blocking_issue").lower():
                errors.append(
                    "Blocked bank-worker contribution row must name missing primary inputs "
                    f"on row {row_number}"
                )
        for column in {"employee_contributions", "employer_contributions"}:
            value = _field(record, column)
            if value:
                _nonnegative(value, column)

    for row_number, record in enumerate(mapping.to_dict("records"), start=2):
        for column in required_mapping_columns:
            if not _field(record, column):
                errors.append(f"Missing {column} on bank-worker mapping row {row_number}")
        if _field(record, "source_registry_status") not in {
            "official_detail_registered",
            "source_acquired",
        }:
            errors.append(f"Unexpected bank-worker mapping source status on row {row_number}")
        if _field(record, "contribution_flow_status") not in allowed_statuses:
            errors.append(f"Unexpected bank-worker mapping flow status on row {row_number}")
        if "pension_fund" not in _field(record, "relationship_to_2011_pension_transfer"):
            errors.append(
                "Bank-worker mapping rows must identify relationship to pension-fund transfer "
                f"on row {row_number}"
            )
    return errors


def validate_bank_asset_liability_outputs(
    audit_path: str,
    asset_trace_path: str,
    sensitivity_path: str,
) -> list[str]:
    """Return validation errors for bank asset-liability audit outputs."""
    audit = pd.read_csv(audit_path, dtype=str)
    asset_trace = pd.read_csv(asset_trace_path, dtype=str)
    sensitivity = pd.read_csv(sensitivity_path, dtype=str)
    errors = [
        *_validate_bank_asset_liability_audit(audit),
        *_validate_bank_asset_trace(asset_trace),
        *_validate_bank_asset_liability_sensitivity(sensitivity),
    ]
    return errors


def validate_bank_special_regime_annual(path: str, *, end_year: int = 2025) -> list[str]:
    """Return validation errors for the annual bank special-regime financing ledger."""
    annual = pd.read_csv(path, dtype=str)
    required_columns = {
        "year",
        "perimeter",
        "unit",
        "price_basis",
        "accounting_basis",
        "state_specific_transfer",
        "pension_expenditure",
        "administrative_cost",
        "attributable_investment_income",
        "asset_drawdown",
        "other_financing",
        "timing_adjustment",
        "reconciliation_residual",
        "source_ids",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(annual.columns))
    if missing_columns:
        return [f"Bank special-regime annual ledger missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = annual[annual.duplicated(subset=["year", "perimeter"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate bank special-regime annual row: "
            f"{_field(duplicate_row, 'year')} {_field(duplicate_row, 'perimeter')}"
        )

    years = sorted(int(year) for year in annual["year"].dropna().astype(str))
    expected_years = list(range(2012, end_year + 1))
    if years != expected_years:
        errors.append(f"Bank special-regime annual ledger must cover 2012-{end_year}")

    allowed_statuses = {
        "blocked_missing_official_annual_components",
        "published_expenditure_benchmark_to_replicate",
        "partial_official_reconciliation",
        "complete",
    }
    nonnegative_columns = {
        "state_specific_transfer",
        "pension_expenditure",
        "administrative_cost",
        "attributable_investment_income",
        "asset_drawdown",
        "other_financing",
    }
    signed_columns = {"timing_adjustment", "reconciliation_residual"}

    for row_number, record in enumerate(annual.to_dict("records"), start=2):
        for column in required_columns.difference(
            {
                "state_specific_transfer",
                "pension_expenditure",
                "administrative_cost",
                "attributable_investment_income",
                "asset_drawdown",
                "other_financing",
                "timing_adjustment",
                "reconciliation_residual",
            }
        ):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank special-regime row {row_number}")
        status = _field(record, "status")
        if status not in allowed_statuses:
            errors.append(f"Unexpected bank special-regime status on row {row_number}: {status}")

        if _field(record, "unit") != "EUR_million":
            errors.append(f"Unexpected unit on bank special-regime row {row_number}")
        if _field(record, "price_basis") != "current_prices":
            errors.append(f"Unexpected price_basis on bank special-regime row {row_number}")

        for column in nonnegative_columns:
            value = _field(record, column)
            if value:
                _nonnegative(value, column)
        for column in signed_columns:
            value = _field(record, column)
            if value:
                _numeric(value, column)

        components = {
            column: _field(record, column)
            for column in {
                "state_specific_transfer",
                "pension_expenditure",
                "administrative_cost",
                "attributable_investment_income",
                "asset_drawdown",
                "other_financing",
                "timing_adjustment",
                "reconciliation_residual",
            }
        }
        if all(components.values()):
            expenditure = float(components["pension_expenditure"]) + float(
                components["administrative_cost"]
            )
            financing = (
                float(components["state_specific_transfer"])
                + float(components["attributable_investment_income"])
                + float(components["asset_drawdown"])
                + float(components["other_financing"])
                + float(components["timing_adjustment"])
            )
            residual = float(components["reconciliation_residual"])
            if not math.isclose(expenditure - financing, residual, rel_tol=0.0, abs_tol=1e-9):
                errors.append(f"Bank special-regime residual identity fails on row {row_number}")
        elif status == "complete":
            errors.append(f"Complete bank special-regime row {row_number} has missing components")
    return errors


def validate_bank_pension_cost_2012(path: str) -> list[str]:
    """Return validation errors for the 2012 transferred-bank pension cost bridge."""
    cost = pd.read_csv(path, dtype=str)
    required_columns = {
        "record_id",
        "year",
        "perimeter",
        "measure",
        "value_eur_million",
        "benchmark_eur_million",
        "residual_vs_benchmark_eur_million",
        "unit",
        "price_basis",
        "accounting_basis",
        "source_ids",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(cost.columns))
    if missing_columns:
        return [f"Bank pension cost 2012 bridge missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = cost[cost.duplicated(subset=["record_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate bank pension cost record_id: {_field(duplicate_row, 'record_id')}"
        )

    allowed_measures = {
        "transfer_current_expenditure_pensions",
        "state_current_transfer_financing",
        "oe_financing_component",
        "cga_bpn_financing_component",
        "administrative_personnel_execution",
        "administrative_goods_services_execution",
        "pension_expenditure_less_state_transfer",
        "unresolved_component_split",
    }
    allowed_statuses = {
        "official_account_reconciles_ec_approximation",
        "official_account_extracted",
        "reconciled_same_report",
        "blocked_missing_component_split",
    }

    for row_number, record in enumerate(cost.to_dict("records"), start=2):
        for column in required_columns.difference(
            {"value_eur_million", "benchmark_eur_million", "residual_vs_benchmark_eur_million"}
        ):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank pension cost row {row_number}")
        if _field(record, "year") != "2012":
            errors.append(f"Bank pension cost row {row_number} must use year 2012")
        if _field(record, "measure") not in allowed_measures:
            errors.append(f"Unexpected bank pension cost measure on row {row_number}")
        status = _field(record, "status")
        if status not in allowed_statuses:
            errors.append(f"Unexpected bank pension cost status on row {row_number}: {status}")
        if _field(record, "unit") != "EUR_million":
            errors.append(f"Unexpected bank pension cost unit on row {row_number}")
        if _field(record, "price_basis") != "current_prices":
            errors.append(f"Unexpected bank pension cost price_basis on row {row_number}")
        if _field(record, "accounting_basis") != "budgetary_public_accounts":
            errors.append(f"Unexpected bank pension cost accounting_basis on row {row_number}")

        value = _field(record, "value_eur_million")
        benchmark = _field(record, "benchmark_eur_million")
        residual = _field(record, "residual_vs_benchmark_eur_million")
        for numeric_value, column in (
            (value, "value_eur_million"),
            (benchmark, "benchmark_eur_million"),
        ):
            if numeric_value:
                _nonnegative(numeric_value, column)
        if residual:
            _numeric(residual, "residual_vs_benchmark_eur_million")
        if value and benchmark and residual:
            expected_residual = float(value) - float(benchmark)
            if not math.isclose(
                expected_residual,
                float(residual),
                rel_tol=0.0,
                abs_tol=0.05,
            ):
                errors.append(f"Bank pension cost benchmark residual fails on row {row_number}")

    measures = set(cost["measure"].dropna().astype(str))
    for measure in {
        "transfer_current_expenditure_pensions",
        "state_current_transfer_financing",
        "pension_expenditure_less_state_transfer",
        "unresolved_component_split",
    }:
        if measure not in measures:
            errors.append(f"Missing bank pension cost measure: {measure}")

    values_by_measure = {
        _field(record, "measure"): _field(record, "value_eur_million")
        for record in cost.to_dict("records")
    }
    expenditure = values_by_measure.get("transfer_current_expenditure_pensions", "")
    financing = values_by_measure.get("state_current_transfer_financing", "")
    residual = values_by_measure.get("pension_expenditure_less_state_transfer", "")
    if expenditure and financing and residual:
        expected_residual = float(expenditure) - float(financing)
        if not math.isclose(expected_residual, float(residual), rel_tol=0.0, abs_tol=0.05):
            errors.append("Bank pension cost financing residual identity fails")

    official_expenditure = cost[
        cost["measure"].astype(str) == "transfer_current_expenditure_pensions"
    ]
    if official_expenditure.empty:
        errors.append("Missing official 2012 bank pension expenditure row")
    else:
        value = _field(official_expenditure.iloc[0], "value_eur_million")
        if not value or not math.isclose(float(value), 516.0, rel_tol=0.0, abs_tol=0.05):
            errors.append(f"Unexpected official 2012 bank pension expenditure: {value}")
    return errors


def validate_bank_transfer_debt_financing_effects(path: str) -> list[str]:
    """Return validation errors for bank-transfer debt and financing-cost effects."""
    debt = pd.read_csv(path, dtype=str)
    required_columns = {
        "record_id",
        "year",
        "perimeter",
        "channel",
        "asset_financing_effect_eur_million",
        "pension_obligation_cost_eur_million",
        "interest_rate",
        "interest_cost_effect_eur_million",
        "unit",
        "price_basis",
        "accounting_basis",
        "source_ids",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(debt.columns))
    if missing_columns:
        return [
            f"Bank transfer debt-financing effects missing columns: {', '.join(missing_columns)}"
        ]

    errors: list[str] = []
    duplicates = debt[debt.duplicated(subset=["record_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate bank transfer debt-financing record_id: "
            f"{_field(duplicate_row, 'record_id')}"
        )

    allowed_statuses = {
        "official_account_extract",
        "aggregate_transfer_registered",
        "reconciled_same_report",
        "sensitivity_observed_rate",
        "blocked_missing_asset_composition",
    }
    required_channels = {
        "recorded_2011_asset_receipt",
        "total_transfer_value",
        "gross_debt_classification_gap",
        "pension_payment_cost",
        "budgetary_financing_and_pension_payment",
        "interest_sensitivity_2011_receipt_programme_loan_rate",
        "interest_sensitivity_2011_receipt_implicit_debt_rate",
        "interest_sensitivity_2011_receipt_10y_treasury_yield",
    }

    for row_number, record in enumerate(debt.to_dict("records"), start=2):
        for column in required_columns.difference(
            {
                "asset_financing_effect_eur_million",
                "pension_obligation_cost_eur_million",
                "interest_rate",
                "interest_cost_effect_eur_million",
            }
        ):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank debt-financing row {row_number}")
        if _field(record, "unit") != "EUR_million":
            errors.append(f"Unexpected bank debt-financing unit on row {row_number}")
        if _field(record, "price_basis") != "current_prices":
            errors.append(f"Unexpected bank debt-financing price_basis on row {row_number}")
        status = _field(record, "status")
        if status not in allowed_statuses:
            errors.append(f"Unexpected bank debt-financing status on row {row_number}: {status}")

        asset = _field(record, "asset_financing_effect_eur_million")
        pension_cost = _field(record, "pension_obligation_cost_eur_million")
        rate = _field(record, "interest_rate")
        interest_effect = _field(record, "interest_cost_effect_eur_million")
        for value, column in (
            (asset, "asset_financing_effect_eur_million"),
            (pension_cost, "pension_obligation_cost_eur_million"),
            (rate, "interest_rate"),
        ):
            if value:
                _nonnegative(value, column)
        if interest_effect:
            _numeric(interest_effect, "interest_cost_effect_eur_million")

        channel = _field(record, "channel")
        if channel.startswith("interest_sensitivity"):
            if not asset or not rate or not interest_effect:
                errors.append(f"Interest sensitivity row {row_number} has missing inputs")
            else:
                expected_effect = -float(asset) * float(rate)
                if not math.isclose(
                    expected_effect,
                    float(interest_effect),
                    rel_tol=0.0,
                    abs_tol=0.0001,
                ):
                    errors.append(
                        f"Bank debt-financing interest identity fails on row {row_number}"
                    )
        if (
            channel == "budgetary_financing_and_pension_payment"
            and asset
            and pension_cost
            and not math.isclose(float(asset), float(pension_cost), rel_tol=0.0, abs_tol=0.05)
        ):
            errors.append("Bank debt-financing 2012 payment and financing mismatch")

    channels = set(debt["channel"].dropna().astype(str))
    for channel in sorted(required_channels.difference(channels)):
        errors.append(f"Missing bank debt-financing channel: {channel}")
    return errors


def validate_bpn_2012_pension_transfer(path: str) -> list[str]:
    """Return validation errors for the separate BPN 2012 pension-transfer case."""
    bpn = pd.read_csv(path, dtype=str)
    required_columns = {
        "record_id",
        "year",
        "case_id",
        "measure",
        "value",
        "unit",
        "receiving_institution",
        "payment_institution",
        "population",
        "perimeter_inclusion",
        "accounting_basis",
        "source_ids",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(bpn.columns))
    if missing_columns:
        return [f"BPN 2012 pension transfer missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = bpn[bpn.duplicated(subset=["record_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(f"Duplicate BPN 2012 record_id: {_field(duplicate_row, 'record_id')}")

    required_measures = {
        "active_worker_rgss_integration",
        "cga_responsibility_current_pensions",
        "cga_responsibility_future_benefits",
        "asset_transfer_to_cga",
        "sams_assets_returned_to_entities",
        "cga_financing_to_ss_2012",
        "pensioners_2012",
        "survivor_pensioners_2012",
        "pensions_paid_by_cga_fund_2012",
        "main_2011_panel_inclusion",
    }
    allowed_statuses = {
        "legal_scope_registered",
        "official_legal_amount_extracted",
        "official_account_extract",
        "panel_boundary_registered",
        "blocked_missing_component_values",
    }
    allowed_units = {"EUR_million", "count", "not_applicable"}

    for row_number, record in enumerate(bpn.to_dict("records"), start=2):
        for column in required_columns.difference({"value", "payment_institution"}):
            if not _field(record, column):
                errors.append(f"Missing {column} on BPN 2012 row {row_number}")
        if _field(record, "year") != "2012":
            errors.append(f"BPN 2012 row {row_number} must use year 2012")
        if _field(record, "case_id") != "bpn_group_dl88":
            errors.append(f"Unexpected BPN case_id on row {row_number}")
        if _field(record, "unit") not in allowed_units:
            errors.append(f"Unexpected BPN unit on row {row_number}")
        status = _field(record, "status")
        if status not in allowed_statuses:
            errors.append(f"Unexpected BPN status on row {row_number}: {status}")
        value = _field(record, "value")
        if value:
            _nonnegative(value, "value")

    measures = set(bpn["measure"].dropna().astype(str))
    for measure in sorted(required_measures.difference(measures)):
        errors.append(f"Missing BPN 2012 measure: {measure}")

    expected_values = {
        "asset_transfer_to_cga": 96.768004,
        "sams_assets_returned_to_entities": 7.31943,
        "cga_financing_to_ss_2012": 0.1359,
        "pensioners_2012": 11.0,
        "survivor_pensioners_2012": 18.0,
        "pensions_paid_by_cga_fund_2012": 0.17927,
    }
    for measure, expected_value in expected_values.items():
        matches = bpn[bpn["measure"].astype(str) == measure]
        if matches.empty:
            continue
        value = _field(matches.iloc[0], "value")
        if not value or not math.isclose(
            float(value),
            expected_value,
            rel_tol=0.0,
            abs_tol=0.0005,
        ):
            errors.append(f"Unexpected BPN value for {measure}: {value}")

    panel_rows = bpn[bpn["measure"].astype(str) == "main_2011_panel_inclusion"]
    if panel_rows.empty:
        errors.append("Missing BPN main-panel boundary row")
    else:
        panel = panel_rows.iloc[0]
        if _field(panel, "perimeter_inclusion") != "excluded_from_2011_dl127_panel":
            errors.append("BPN case must remain excluded from the main 2011 DL127 panel")
        if _field(panel, "receiving_institution") != "CGA":
            errors.append("BPN panel-boundary row must identify CGA as receiving institution")
    return errors


def validate_bank_benefit_risk_distribution(path: str) -> list[str]:
    """Return validation errors for bank-transfer benefit and risk distribution outputs."""
    distribution = pd.read_csv(path, dtype=str)
    required_columns = {
        "record_id",
        "year",
        "institution",
        "channel",
        "value",
        "unit",
        "price_basis",
        "accounting_basis",
        "bank_effect",
        "public_sector_effect",
        "risk_holder_after_transfer",
        "source_ids",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(distribution.columns))
    if missing_columns:
        return [f"Bank benefit-risk distribution missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = distribution[distribution.duplicated(subset=["record_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate bank benefit-risk record_id: {_field(duplicate_row, 'record_id')}"
        )

    allowed_channels = {
        "balance_sheet_relief",
        "liquidity_effect",
        "actuarial_risk_transfer",
        "retained_bank_responsibilities",
        "fiscal_accounting_effect",
        "demonstrable_net_subsidy",
        "bank_level_net_position",
    }
    allowed_statuses = {
        "legal_channel_identified",
        "partial_aggregate_extract",
        "accounting_treatment_to_replicate",
        "blocked_no_subsidy_classification",
        "blocked_missing_bank_level_values",
        "complete",
    }

    for row_number, record in enumerate(distribution.to_dict("records"), start=2):
        for column in required_columns.difference({"value"}):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank benefit-risk row {row_number}")
        channel = _field(record, "channel")
        if channel not in allowed_channels:
            errors.append(f"Unexpected bank benefit-risk channel on row {row_number}: {channel}")
        status = _field(record, "status")
        if status not in allowed_statuses:
            errors.append(f"Unexpected bank benefit-risk status on row {row_number}: {status}")
        if _field(record, "unit") != "EUR_million":
            errors.append(f"Unexpected unit on bank benefit-risk row {row_number}")
        if _field(record, "price_basis") != "current_prices":
            errors.append(f"Unexpected price_basis on bank benefit-risk row {row_number}")
        value = _field(record, "value")
        if value:
            _nonnegative(value, "value")

    bank_level = distribution[distribution["channel"].astype(str) == "bank_level_net_position"]
    if len(bank_level) != 18:
        errors.append(f"Expected 18 bank-level net-position rows, found {len(bank_level)}")
    bank_level_statuses = set(bank_level["status"].dropna().astype(str))
    if bank_level_statuses.difference({"blocked_missing_bank_level_values"}):
        errors.append("Bank-level net-position rows must remain blocked until values are acquired")

    required_channels = allowed_channels.difference({"bank_level_net_position"})
    channels = set(distribution["channel"].dropna().astype(str))
    for channel in sorted(required_channels.difference(channels)):
        errors.append(f"Missing bank benefit-risk channel: {channel}")

    subsidy = distribution[distribution["channel"].astype(str) == "demonstrable_net_subsidy"]
    if subsidy.empty:
        errors.append("Missing demonstrable net-subsidy classification row")
    else:
        for _, subsidy_record in subsidy.iterrows():
            if _field(subsidy_record, "value"):
                errors.append("Demonstrable net-subsidy row must not have a value while blocked")
            if _field(subsidy_record, "status") != "blocked_no_subsidy_classification":
                errors.append("Demonstrable net-subsidy row must remain blocked")
    return errors


def validate_bank_esa_treatment_bridge(path: str) -> list[str]:
    """Return validation errors for the ESA-95/ESA-2010 bank-transfer bridge."""
    bridge = pd.read_csv(path, dtype=str)
    required_columns = {
        "record_id",
        "year",
        "transaction",
        "esa_standard",
        "classification",
        "deficit_effect_direction",
        "deficit_effect_percent_gdp",
        "amount_eur_million",
        "implied_gdp_eur_million",
        "unit",
        "source_ids",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(bridge.columns))
    if missing_columns:
        return [f"Bank ESA treatment bridge missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = bridge[bridge.duplicated(subset=["record_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(f"Duplicate bank ESA bridge record_id: {_field(duplicate_row, 'record_id')}")

    allowed_standards = {"ESA-95", "ESA-2010", "bridge"}
    allowed_directions = {"deficit_decreasing", "no_direct_deficit_impact", "not_applicable"}
    allowed_statuses = {
        "replicated_from_cge_and_ec",
        "classification_confirmed_from_ec",
        "interpretive_bridge",
        "blocked_missing_machine_readable_accounts",
    }

    for row_number, record in enumerate(bridge.to_dict("records"), start=2):
        for column in required_columns.difference(
            {"deficit_effect_percent_gdp", "amount_eur_million", "implied_gdp_eur_million"}
        ):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank ESA bridge row {row_number}")
        standard = _field(record, "esa_standard")
        if standard not in allowed_standards:
            errors.append(f"Unexpected ESA standard on bank ESA bridge row {row_number}")
        direction = _field(record, "deficit_effect_direction")
        if direction not in allowed_directions:
            errors.append(
                f"Unexpected deficit effect direction on bank ESA bridge row {row_number}"
            )
        status = _field(record, "status")
        if status not in allowed_statuses:
            errors.append(f"Unexpected bank ESA bridge status on row {row_number}: {status}")

        percent = _field(record, "deficit_effect_percent_gdp")
        amount = _field(record, "amount_eur_million")
        implied_gdp = _field(record, "implied_gdp_eur_million")
        for value, name in (
            (percent, "deficit_effect_percent_gdp"),
            (amount, "amount_eur_million"),
            (implied_gdp, "implied_gdp_eur_million"),
        ):
            if value:
                _nonnegative(value, name)

        if amount and percent and implied_gdp:
            reconstructed_percent = float(amount) / float(implied_gdp) * 100.0
            if not math.isclose(
                reconstructed_percent,
                float(percent),
                rel_tol=0.0,
                abs_tol=0.05,
            ):
                errors.append(f"Bank ESA bridge percent identity fails on row {row_number}")

    standards = set(bridge["esa_standard"].dropna().astype(str))
    for standard in ("ESA-95", "ESA-2010", "bridge"):
        if standard not in standards:
            errors.append(f"Missing ESA bridge standard: {standard}")

    esa2010 = bridge[bridge["esa_standard"].astype(str) == "ESA-2010"]
    if esa2010.empty:
        errors.append("Missing ESA-2010 bank transfer classification row")
    else:
        for _, esa2010_record in esa2010.iterrows():
            if _field(esa2010_record, "deficit_effect_direction") != "no_direct_deficit_impact":
                errors.append("ESA-2010 row must have no direct deficit impact")
            effect = _field(esa2010_record, "deficit_effect_percent_gdp")
            if effect and not math.isclose(float(effect), 0.0, rel_tol=0.0, abs_tol=1e-12):
                errors.append("ESA-2010 direct deficit effect must be zero when populated")
    return errors


def _validate_bank_asset_liability_audit(audit: pd.DataFrame) -> list[str]:
    required_columns = {
        "audit_id",
        "year",
        "institution",
        "unit",
        "price_basis",
        "accounting_basis",
        "liability_pv_legal_4pct",
        "assets_transferred_total",
        "cash_transferred",
        "portuguese_public_debt_transferred",
        "other_assets_transferred",
        "statutory_equality_residual",
        "discount_rate_sensitivity_min",
        "discount_rate_sensitivity_max",
        "mortality_sensitivity_status",
        "source_ids",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(audit.columns))
    if missing_columns:
        return [f"Bank asset-liability audit missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = audit[audit.duplicated(subset=["audit_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate bank asset-liability audit_id: {_field(duplicate_row, 'audit_id')}"
        )

    for row_number, record in enumerate(audit.to_dict("records"), start=2):
        for column in required_columns.difference(
            {
                "liability_pv_legal_4pct",
                "assets_transferred_total",
                "cash_transferred",
                "portuguese_public_debt_transferred",
                "other_assets_transferred",
                "statutory_equality_residual",
            }
        ):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank asset-liability audit row {row_number}")
        status = _field(record, "status")
        if status not in {"partial_aggregate_extract", "complete"}:
            errors.append(
                f"Unexpected bank asset-liability audit status on row {row_number}: {status}"
            )
        for column in {
            "liability_pv_legal_4pct",
            "assets_transferred_total",
            "cash_transferred",
            "portuguese_public_debt_transferred",
            "other_assets_transferred",
            "discount_rate_sensitivity_min",
            "discount_rate_sensitivity_max",
        }:
            value = _field(record, column)
            if value:
                _nonnegative(value, column)
        residual = _field(record, "statutory_equality_residual")
        if residual:
            _numeric(residual, "statutory_equality_residual")

    operation = audit[audit["audit_id"] == "BANK_AL_AGG_2011_OPERATION"]
    receipt = audit[audit["audit_id"] == "BANK_AL_AGG_2011_STATE_RECEIPT"]
    if operation.empty or not math.isclose(
        float(_field(operation.iloc[0], "liability_pv_legal_4pct")),
        5993.2,
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        errors.append("Missing CGE 2011 aggregate operation value 5993.2")
    if receipt.empty or not math.isclose(
        float(_field(receipt.iloc[0], "assets_transferred_total")),
        3263.1,
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        errors.append("Missing CGE 2011 recorded State receipt value 3263.1")
    return errors


def _validate_bank_asset_trace(asset_trace: pd.DataFrame) -> list[str]:
    required_columns = {
        "institution",
        "asset_type",
        "transfer_value",
        "destination",
        "accounting_treatment",
        "source_id",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(asset_trace.columns))
    if missing_columns:
        return [f"Bank asset trace missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    blocked_count = int(
        (asset_trace["status"].astype(str) == "blocked_missing_bank_level_values").sum()
    )
    if blocked_count != 18:
        errors.append(f"Expected 18 blocked bank-level asset rows, found {blocked_count}")
    aggregate = asset_trace[asset_trace["institution"] == "aggregate_banking_sector"]
    if aggregate.empty or not math.isclose(
        float(_field(aggregate.iloc[0], "transfer_value")),
        3263.1,
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        errors.append("Missing aggregate bank asset trace value 3263.1")

    for row_number, record in enumerate(asset_trace.to_dict("records"), start=2):
        for column in required_columns.difference({"transfer_value"}):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank asset trace row {row_number}")
        value = _field(record, "transfer_value")
        if value:
            _nonnegative(value, "transfer_value")
    return errors


def _validate_bank_asset_liability_sensitivity(sensitivity: pd.DataFrame) -> list[str]:
    required_columns = {
        "scenario_id",
        "institution",
        "discount_rate",
        "mortality_assumption",
        "liability_pv",
        "delta_vs_legal_4pct",
        "unit",
        "source_ids",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(sensitivity.columns))
    if missing_columns:
        return [f"Bank asset-liability sensitivity missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    rates = sorted(float(value) for value in sensitivity["discount_rate"].dropna().astype(str))
    if rates != [0.02, 0.03, 0.04, 0.05, 0.06]:
        errors.append("Bank asset-liability sensitivity must cover discount rates 0.02-0.06")
    for row_number, record in enumerate(sensitivity.to_dict("records"), start=2):
        for column in required_columns.difference({"liability_pv", "delta_vs_legal_4pct"}):
            if not _field(record, column):
                errors.append(f"Missing {column} on bank sensitivity row {row_number}")
        status = _field(record, "status")
        if status not in {"blocked_missing_cashflow_and_demographic_inputs", "complete"}:
            errors.append(f"Unexpected bank sensitivity status on row {row_number}: {status}")
        for column in {"liability_pv", "discount_rate"}:
            value = _field(record, column)
            if value:
                _nonnegative(value, column)
        delta = _field(record, "delta_vs_legal_4pct")
        if delta:
            _numeric(delta, "delta_vs_legal_4pct")
    return errors


def _numeric(value: str, name: str) -> float:
    try:
        numeric = float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    return numeric


def _nonnegative(value: str, name: str) -> float:
    numeric = _numeric(value, name)
    if numeric < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return numeric


def _field(row: Any, column: str) -> str:
    value = row[column]
    if pd.isna(value):
        return ""
    return str(value).strip()
