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
