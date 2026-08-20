"""Transparent accounting identities used by the research notebooks."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True, slots=True)
class FinancingIdentityResult:
    """Result of an annual financing reconciliation.

    Attributes:
        total_financing: Sum of contribution, transfer and other financing inflows.
        total_use: Sum of benefit, administrative and other expenditure outflows.
        residual: Financing minus uses minus the reported change in financial position.
        reconciled: Whether the absolute residual is within the supplied tolerance.
    """

    total_financing: float
    total_use: float
    residual: float
    reconciled: bool


def _finite_nonnegative(value: float, name: str) -> float:
    """Validate a non-negative finite monetary input."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    if numeric < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return numeric


def reconcile_financing_identity(
    *,
    employee_contributions: float,
    employer_contributions: float,
    state_transfers: float,
    other_financing: float,
    pension_expenditure: float,
    administrative_expenditure: float,
    other_expenditure: float,
    change_in_financial_position: float,
    tolerance: float = 1.0,
) -> FinancingIdentityResult:
    """Reconcile a transparent annual pension-financing identity.

    The identity is::

        financing = expenditure + change_in_financial_position + residual

    A positive residual means recorded financing exceeds recorded uses plus the reported
    change in financial position. The function does not attach an economic interpretation
    to the residual; classification and timing differences must be investigated separately.
    """
    inflows = (
        _finite_nonnegative(employee_contributions, "employee_contributions"),
        _finite_nonnegative(employer_contributions, "employer_contributions"),
        _finite_nonnegative(state_transfers, "state_transfers"),
        _finite_nonnegative(other_financing, "other_financing"),
    )
    outflows = (
        _finite_nonnegative(pension_expenditure, "pension_expenditure"),
        _finite_nonnegative(administrative_expenditure, "administrative_expenditure"),
        _finite_nonnegative(other_expenditure, "other_expenditure"),
    )
    if not isinstance(change_in_financial_position, (int, float)):
        raise TypeError("change_in_financial_position must be numeric")
    change = float(change_in_financial_position)
    if not math.isfinite(change):
        raise ValueError("change_in_financial_position must be finite")
    tol = _finite_nonnegative(tolerance, "tolerance")

    total_financing = sum(inflows)
    total_use = sum(outflows)
    residual = total_financing - total_use - change
    return FinancingIdentityResult(
        total_financing=total_financing,
        total_use=total_use,
        residual=residual,
        reconciled=abs(residual) <= tol,
    )


def validate_cga_financing_ledger(path: str) -> list[str]:
    """Return validation errors for the processed CGA financing ledger."""
    ledger = pd.read_csv(path, dtype=str)
    required_columns = {
        "year",
        "source_id",
        "unit",
        "price_basis",
        "accounting_basis",
        "perimeter",
        "employee_quotations",
        "employer_contributions",
        "state_budget_transfers",
        "other_public_transfers",
        "investment_income",
        "pension_expenditure",
        "other_benefits",
        "administration",
        "contributor_count",
        "pensioner_count",
        "contribution_base_payroll",
        "published_additional_state_transfer",
        "reported_global_balance",
        "pt_pension_fund_effect",
        "reported_global_balance_ex_pt_fund",
        "identity_residual",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(ledger.columns))
    if missing_columns:
        return [f"CGA financing ledger missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = ledger[ledger.duplicated(subset=["year", "source_id", "perimeter"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate CGA financing ledger row: "
            f"{_field(duplicate_row, 'year')} {_field(duplicate_row, 'perimeter')}"
        )

    complete_components = {
        "employee_quotations",
        "employer_contributions",
        "state_budget_transfers",
        "other_public_transfers",
        "investment_income",
        "pension_expenditure",
        "other_benefits",
        "administration",
        "identity_residual",
    }
    optional_numeric = {
        "contributor_count",
        "pensioner_count",
        "contribution_base_payroll",
        "published_additional_state_transfer",
        "reported_global_balance",
        "pt_pension_fund_effect",
        "reported_global_balance_ex_pt_fund",
    }
    for row_number, record in enumerate(ledger.to_dict("records"), start=2):
        for column in required_columns.difference({"identity_residual"}):
            if column in complete_components or column in optional_numeric:
                continue
            if not _field(record, column):
                errors.append(f"Missing {column} on CGA financing ledger row {row_number}")
        status = _field(record, "status")
        if status == "complete":
            for column in complete_components:
                if not _field(record, column):
                    errors.append(f"Complete CGA ledger row {row_number} missing {column}")
        elif not status.startswith("partial"):
            errors.append(f"Unexpected CGA financing ledger status on row {row_number}: {status}")

        for column in complete_components.union(optional_numeric):
            value = _field(record, column)
            if value:
                _numeric(value, column)
    return errors


def validate_pension_flow_of_funds(path: str) -> list[str]:
    """Return validation errors for the long-form pension flow-of-funds matrix."""
    matrix = pd.read_csv(path, dtype=str)
    required_columns = {
        "record_id",
        "year",
        "transaction_id",
        "from_entity",
        "to_entity",
        "flow_type",
        "stock_flow",
        "value",
        "unit",
        "price_basis",
        "accounting_basis",
        "source_ids",
        "consolidation_scope",
        "consolidates_in_general_government",
        "bridge_definition_id",
        "bridge_component",
        "bridge_sign",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(matrix.columns))
    if missing_columns:
        return [f"Pension flow-of-funds matrix missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicated_ids = matrix[matrix.duplicated(subset=["record_id"], keep=False)]
    for _, duplicate_row in duplicated_ids.iterrows():
        errors.append(f"Duplicate pension flow row: {_field(duplicate_row, 'record_id')}")

    entities = {
        "households_workers",
        "public_employers",
        "private_banks",
        "private_pension_funds",
        "cga",
        "social_security",
        "fefss",
        "state_budget_treasury",
        "consolidated_general_government",
    }
    observed_entities = set(matrix["from_entity"].dropna()).union(set(matrix["to_entity"].dropna()))
    missing_entities = sorted(entities.difference(observed_entities))
    if missing_entities:
        errors.append(f"Pension flow matrix missing entities: {', '.join(missing_entities)}")

    allowed_stock_flow = {"flow", "stock", "balance", "memo"}
    allowed_units = {"EUR_million", "count", "not_applicable"}
    allowed_consolidation = {"yes", "no", "not_applicable"}
    general_government_entities = {
        "cga",
        "social_security",
        "fefss",
        "state_budget_treasury",
        "public_employers",
        "consolidated_general_government",
    }
    bridge_keys: set[tuple[str, str]] = set()

    for row_number, record in enumerate(matrix.to_dict("records"), start=2):
        for column in required_columns.difference({"value", "source_ids", "bridge_sign"}):
            if not _field(record, column):
                errors.append(f"Missing {column} on pension flow row {row_number}")

        for column in ("from_entity", "to_entity"):
            entity = _field(record, column)
            if entity and entity not in entities:
                errors.append(f"Unknown {column} on pension flow row {row_number}: {entity}")

        stock_flow = _field(record, "stock_flow")
        if stock_flow and stock_flow not in allowed_stock_flow:
            errors.append(f"Unexpected stock_flow on pension flow row {row_number}: {stock_flow}")

        unit = _field(record, "unit")
        if unit and unit not in allowed_units:
            errors.append(f"Unexpected unit on pension flow row {row_number}: {unit}")

        consolidation = _field(record, "consolidates_in_general_government")
        if consolidation and consolidation not in allowed_consolidation:
            errors.append(
                "Unexpected consolidates_in_general_government on pension flow row "
                f"{row_number}: {consolidation}"
            )
        if consolidation == "yes" and (
            _field(record, "from_entity") not in general_government_entities
            or _field(record, "to_entity") not in general_government_entities
        ):
            errors.append(
                f"Consolidating pension flow row {row_number} must stay inside general government"
            )

        value = _field(record, "value")
        status = _field(record, "status")
        if value:
            _numeric(value, "value")
        elif not (
            status.startswith("blocked") or status == "scope_registered" or unit == "not_applicable"
        ):
            errors.append(f"Missing value on pension flow row {row_number}")

        bridge_id = _field(record, "bridge_definition_id")
        bridge_component = _field(record, "bridge_component")
        if bridge_id != "not_applicable":
            if not value:
                errors.append(f"Bridge row {row_number} must have a numeric value")
            sign = _field(record, "bridge_sign")
            if sign not in {"-1", "1"}:
                errors.append(f"Bridge row {row_number} must use bridge_sign -1 or 1")
            bridge_key = (bridge_id, bridge_component)
            if bridge_key in bridge_keys:
                errors.append(
                    f"Duplicate pension flow bridge component: {bridge_id} {bridge_component}"
                )
            bridge_keys.add(bridge_key)
        elif bridge_component != "not_applicable":
            errors.append(
                f"Non-bridge pension flow row {row_number} must use not_applicable component"
            )

    errors.extend(_validate_flow_bridge_identities(matrix))
    return errors


def _validate_flow_bridge_identities(matrix: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    bridge = matrix[matrix["bridge_definition_id"].fillna("") != "not_applicable"].copy()
    if bridge.empty:
        return ["Pension flow matrix has no bridge rows"]
    bridge["value_numeric"] = pd.to_numeric(bridge["value"], errors="coerce")

    cga = _bridge_values(bridge, "cga_2011_balance_decomposition")
    required_cga = {
        "reported_global_balance",
        "pt_pension_fund_effect",
        "reported_global_balance_ex_pt_fund",
    }
    if required_cga.issubset(cga):
        residual = cga["reported_global_balance"] - (
            cga["pt_pension_fund_effect"] + cga["reported_global_balance_ex_pt_fund"]
        )
        if abs(residual) > 0.11:
            errors.append(
                "CGA 2011 flow bridge does not reconcile within one-decimal rounding tolerance"
            )
    else:
        errors.append("CGA 2011 flow bridge is missing required components")

    bank_cash = _bridge_values(bridge, "bank_2012_cash_identity")
    required_bank_cash = {"state_current_transfer_financing", "pension_payment_current_expenditure"}
    if required_bank_cash.issubset(bank_cash):
        residual = (
            bank_cash["state_current_transfer_financing"]
            - bank_cash["pension_payment_current_expenditure"]
        )
        if abs(residual) > 0.01:
            errors.append("Bank 2012 cash flow bridge does not reconcile")
    else:
        errors.append("Bank 2012 cash flow bridge is missing required components")

    financing_split = _bridge_values(bridge, "bank_2012_financing_split")
    required_split = {"oe_financing_component", "cga_bpn_financing_component"}
    if required_split.issubset(financing_split):
        component_total = (
            financing_split["oe_financing_component"]
            + financing_split["cga_bpn_financing_component"]
        )
        if abs(component_total - 516.0) > 0.1:
            errors.append("Bank 2012 financing split does not match the rounded total")
    else:
        errors.append("Bank 2012 financing split is missing required components")

    return errors


def _bridge_values(matrix: pd.DataFrame, bridge_id: str) -> dict[str, float]:
    subset = matrix[matrix["bridge_definition_id"] == bridge_id]
    return {
        str(record["bridge_component"]): float(record["value_numeric"])
        for record in subset.to_dict("records")
        if not pd.isna(record["value_numeric"])
    }


def validate_employee_remittance_audit(path: str) -> list[str]:
    """Return validation errors for the employee remittance audit table."""
    audit = pd.read_csv(path, dtype=str)
    required_columns = {
        "year",
        "perimeter",
        "unit",
        "price_basis",
        "accounting_basis",
        "legal_worker_rate_total",
        "legal_worker_liability",
        "withheld_from_payroll",
        "recorded_cga_worker_revenue",
        "timing_adjustments",
        "arrears_corrections",
        "base_definition_adjustment",
        "perimeter_adjustment",
        "unexplained_remittance_gap",
        "source_ids",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(audit.columns))
    if missing_columns:
        return [f"Employee remittance audit missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = audit[audit.duplicated(subset=["year", "perimeter"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate employee remittance audit row: "
            f"{_field(duplicate_row, 'year')} {_field(duplicate_row, 'perimeter')}"
        )

    complete_fields = {
        "legal_worker_liability",
        "withheld_from_payroll",
        "recorded_cga_worker_revenue",
        "timing_adjustments",
        "arrears_corrections",
        "base_definition_adjustment",
        "perimeter_adjustment",
        "unexplained_remittance_gap",
    }
    for row_number, record in enumerate(audit.to_dict("records"), start=2):
        for column in required_columns.difference(complete_fields):
            if not _field(record, column):
                errors.append(f"Missing {column} on employee remittance audit row {row_number}")
        status = _field(record, "status")
        if status == "complete":
            for column in complete_fields:
                if not _field(record, column):
                    errors.append(f"Complete employee remittance row {row_number} missing {column}")
        elif not status.startswith("blocked"):
            errors.append(
                f"Unexpected employee remittance audit status on row {row_number}: {status}"
            )

        for column in complete_fields.union({"legal_worker_rate_total"}):
            value = _field(record, column)
            if value:
                _numeric(value, column)
    return errors


def validate_employer_contribution_audit(path: str) -> list[str]:
    """Return validation errors for the employer contribution audit table."""
    audit = pd.read_csv(path, dtype=str)
    required_columns = {
        "year",
        "employer_class",
        "unit",
        "price_basis",
        "accounting_basis",
        "legal_employer_rate_total",
        "legal_due",
        "recorded_cga_employer_revenue",
        "timing_adjustments",
        "arrears_corrections",
        "base_definition_adjustment",
        "perimeter_adjustment",
        "legal_compliance_gap",
        "economic_benchmark_rate_total",
        "economic_benchmark_due",
        "economic_benchmark_gap",
        "source_ids",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(audit.columns))
    if missing_columns:
        return [f"Employer contribution audit missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = audit[audit.duplicated(subset=["year", "employer_class"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate employer contribution audit row: "
            f"{_field(duplicate_row, 'year')} {_field(duplicate_row, 'employer_class')}"
        )

    complete_fields = {
        "legal_due",
        "recorded_cga_employer_revenue",
        "timing_adjustments",
        "arrears_corrections",
        "base_definition_adjustment",
        "perimeter_adjustment",
        "legal_compliance_gap",
        "economic_benchmark_due",
        "economic_benchmark_gap",
    }
    for row_number, record in enumerate(audit.to_dict("records"), start=2):
        for column in required_columns.difference(complete_fields):
            if not _field(record, column):
                errors.append(f"Missing {column} on employer contribution audit row {row_number}")

        notes = _field(record, "notes").lower()
        if "not a legal debt" not in notes:
            errors.append(
                "Employer contribution audit row "
                f"{row_number} must state that the economic benchmark is not a legal debt"
            )

        status = _field(record, "status")
        if status == "complete":
            for column in complete_fields:
                if not _field(record, column):
                    errors.append(
                        f"Complete employer contribution row {row_number} missing {column}"
                    )
        elif not status.startswith("blocked"):
            errors.append(
                f"Unexpected employer contribution audit status on row {row_number}: {status}"
            )

        for column in complete_fields.union(
            {"legal_employer_rate_total", "economic_benchmark_rate_total"}
        ):
            value = _field(record, column)
            if value:
                _numeric(value, column)
    return errors


def _numeric(value: str, name: str) -> float:
    try:
        numeric = float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    return numeric


def _field(row: Any, column: str) -> str:
    value = row[column]
    if pd.isna(value):
        return ""
    return str(value).strip()
