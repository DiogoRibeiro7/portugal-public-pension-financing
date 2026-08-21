"""Transparent accounting identities used by the research notebooks."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date
from typing import Any

import pandas as pd

STATE_FINANCING_REQUIRED_COLUMNS = frozenset(
    {
        "rule_id",
        "valid_from",
        "valid_to",
        "institution",
        "transfer_type",
        "state_role",
        "legal_basis",
        "calculation_rule",
        "recipient",
        "accounting_basis",
        "source_id",
        "status",
        "notes",
    }
)

STATE_FINANCING_TRANSFER_TYPES = frozenset(
    {
        "accounting_presentation_rule",
        "budget_appropriation_route",
        "specific_state_transfer",
        "transferred_asset_financing",
    }
)

STATE_FINANCING_STATE_ROLES = frozenset(
    {
        "accounting_presenter",
        "asset_recipient",
        "budget_authority",
        "guarantor",
    }
)

STATE_FINANCING_STATUSES = frozenset(
    {
        "accounting_presentation_observed",
        "legal_rule_and_account_observed",
        "legal_rule_observed",
        "official_account_extract",
        "source_route_registered",
    }
)


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


def validate_cga_financing_ledger(
    path: str,
    source_registry_path: str | None = None,
) -> list[str]:
    """Return validation errors for the processed CGA financing ledger."""
    ledger = pd.read_csv(path, dtype=str, keep_default_na=False)
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
        "full_identity_status",
        "balance_decomposition_residual",
        "missing_components",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(ledger.columns))
    if missing_columns:
        return [f"CGA financing ledger missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    observed_years = {int(year) for year in ledger["year"] if str(year).isdigit()}
    missing_years = sorted(set(range(1977, 2026)).difference(observed_years))
    if missing_years:
        errors.append(
            f"CGA financing ledger missing years: {', '.join(str(year) for year in missing_years)}"
        )

    duplicates = ledger[ledger.duplicated(subset=["year", "source_id", "perimeter"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate CGA financing ledger row: "
            f"{_field(duplicate_row, 'year')} {_field(duplicate_row, 'perimeter')}"
        )

    source_ids = _source_ids(source_registry_path)
    allowed_statuses = {
        "blocked_missing_primary_account_components",
        "complete",
        "partial_cge_extract",
    }
    allowed_identity_statuses = {"blocked_missing_components", "reconciled"}
    allowed_units = {"EUR_million", "mixed"}
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
        "balance_decomposition_residual",
    }
    required_missing_components = complete_components.difference({"identity_residual"})
    for row_number, record in enumerate(ledger.to_dict("records"), start=2):
        for column in required_columns.difference({"identity_residual"}):
            if column in complete_components or column in optional_numeric:
                continue
            if not _field(record, column):
                errors.append(f"Missing {column} on CGA financing ledger row {row_number}")

        for source_id in _field(record, "source_id").split(";"):
            if source_ids is not None and source_id and source_id not in source_ids:
                errors.append(
                    f"CGA financing ledger row {row_number} unknown source_id: {source_id}"
                )

        unit = _field(record, "unit")
        if unit and unit not in allowed_units:
            errors.append(f"Unexpected CGA financing ledger unit on row {row_number}: {unit}")

        identity_status = _field(record, "full_identity_status")
        if identity_status and identity_status not in allowed_identity_statuses:
            errors.append(
                f"Unexpected CGA financing identity status on row {row_number}: {identity_status}"
            )

        status = _field(record, "status")
        if status == "complete":
            for column in complete_components:
                if not _field(record, column):
                    errors.append(f"Complete CGA ledger row {row_number} missing {column}")
            if identity_status != "reconciled":
                errors.append(f"Complete CGA ledger row {row_number} must reconcile identity")
        elif status in {"blocked_missing_primary_account_components", "partial_cge_extract"}:
            missing_components = set(_field(record, "missing_components").split(";"))
            for component in sorted(required_missing_components.difference(missing_components)):
                errors.append(
                    f"Incomplete CGA ledger row {row_number} missing blocker for {component}"
                )
            if identity_status != "blocked_missing_components":
                errors.append(f"Incomplete CGA ledger row {row_number} must block full identity")
        elif status not in allowed_statuses:
            errors.append(f"Unexpected CGA financing ledger status on row {row_number}: {status}")

        for column in complete_components.union(optional_numeric):
            value = _field(record, column)
            if value:
                _numeric(value, column)
        errors.extend(_validate_cga_balance_decomposition(record, row_number))
        errors.extend(_validate_cga_complete_identity(record, row_number))
    return errors


def validate_cga_closed_scheme_decomposition(path: str) -> list[str]:
    """Return validation errors for the CGA closed-scheme decomposition ledger."""
    ledger = pd.read_csv(path, dtype=str)
    required_columns = {
        "record_id",
        "year",
        "driver",
        "identity_role",
        "observed_value",
        "counterfactual_value",
        "balance_effect_value",
        "unit",
        "price_basis",
        "accounting_basis",
        "perimeter",
        "source_ids",
        "status",
        "blocking_issue",
        "causal_claim_permitted",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(ledger.columns))
    if missing_columns:
        return [f"CGA closed-scheme decomposition missing columns: {', '.join(missing_columns)}"]

    required_drivers = {
        "average_pension_and_survivor_benefit",
        "closed_scheme_cash_balance",
        "contribution_base_payroll",
        "contributor_count",
        "pensioner_count",
        "policy_contribution_rate",
        "residual_attribution_boundary",
        "state_and_other_transfers",
    }
    observed_drivers = set(ledger["driver"].dropna().astype(str))
    errors: list[str] = []
    for driver in sorted(required_drivers.difference(observed_drivers)):
        errors.append(f"Missing CGA closed-scheme driver: {driver}")

    duplicates = ledger[ledger.duplicated(subset=["record_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(f"Duplicate CGA closed-scheme row: {_field(duplicate_row, 'record_id')}")

    allowed_statuses = {
        "blocked_missing_inputs",
        "complete",
        "identity_registered",
        "partial_bounded_reconstruction",
    }
    allowed_units = {"EUR_million", "count", "not_applicable", "percent", "ratio"}
    for row_number, record in enumerate(ledger.to_dict("records"), start=2):
        record_id = _field(record, "record_id") or f"row {row_number}"
        for column in required_columns.difference(
            {"observed_value", "counterfactual_value", "balance_effect_value"}
        ):
            if not _field(record, column):
                errors.append(f"Missing {column} on CGA closed-scheme row {row_number}")

        status = _field(record, "status")
        if status and status not in allowed_statuses:
            errors.append(f"Unexpected CGA closed-scheme status on row {row_number}: {status}")
        if status.startswith("blocked") and _field(record, "blocking_issue") in {"", "none"}:
            errors.append(f"Blocked CGA closed-scheme row {record_id} must name a blocker")

        causal_claim = _field(record, "causal_claim_permitted")
        if causal_claim not in {"no", "yes"}:
            errors.append(f"CGA closed-scheme row {record_id} must use yes/no causal claim flag")
        if status != "complete" and causal_claim != "no":
            errors.append(f"Incomplete CGA closed-scheme row {record_id} cannot permit causality")

        unit = _field(record, "unit")
        if unit and unit not in allowed_units:
            errors.append(f"Unexpected CGA closed-scheme unit on row {row_number}: {unit}")

        for column in ("observed_value", "counterfactual_value", "balance_effect_value"):
            value = _field(record, column)
            if value:
                _numeric(value, column)
        if status == "complete" and not _field(record, "balance_effect_value"):
            errors.append(f"Complete CGA closed-scheme row {record_id} missing balance effect")

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


def validate_state_financing_rule_registry(path: str, source_registry_path: str) -> list[str]:
    """Return validation errors for bounded State-financing rule records."""
    registry = pd.read_csv(path, dtype=str, keep_default_na=False)
    sources = pd.read_csv(source_registry_path, dtype=str, keep_default_na=False)
    missing_columns = sorted(STATE_FINANCING_REQUIRED_COLUMNS.difference(registry.columns))
    if missing_columns:
        return [f"State financing rule registry missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    if len(registry) < 5:
        errors.append("State financing rule registry must contain at least 5 rule rows")

    duplicate_ids = registry[registry.duplicated(subset=["rule_id"], keep=False)]
    for _, duplicate_row in duplicate_ids.iterrows():
        errors.append(f"Duplicate state financing rule row: {_field(duplicate_row, 'rule_id')}")

    observed_transfer_types = set(registry["transfer_type"])
    for transfer_type in sorted(STATE_FINANCING_TRANSFER_TYPES.difference(observed_transfer_types)):
        errors.append(f"Missing State financing transfer type: {transfer_type}")

    source_ids = set(sources["source_id"])
    for row_number, record in enumerate(registry.to_dict("records"), start=2):
        rule_id = _field(record, "rule_id") or f"row {row_number}"
        for column in STATE_FINANCING_REQUIRED_COLUMNS.difference({"valid_to"}):
            if not _field(record, column):
                errors.append(f"Missing {column} on State financing row {row_number}")

        transfer_type = _field(record, "transfer_type")
        if transfer_type and transfer_type not in STATE_FINANCING_TRANSFER_TYPES:
            errors.append(
                f"Unexpected State financing transfer_type on row {row_number}: {transfer_type}"
            )

        state_role = _field(record, "state_role")
        if state_role and state_role not in STATE_FINANCING_STATE_ROLES:
            errors.append(
                f"Unexpected State financing state_role on row {row_number}: {state_role}"
            )

        status = _field(record, "status")
        if status and status not in STATE_FINANCING_STATUSES:
            errors.append(f"Unexpected State financing status on row {row_number}: {status}")

        for source_id in _field(record, "source_id").split(";"):
            if source_id and source_id not in source_ids:
                errors.append(
                    f"State financing row {rule_id} references unknown source_id: {source_id}"
                )

        valid_from = _date_field(record, "valid_from", rule_id, errors)
        valid_to_text = _field(record, "valid_to")
        if valid_to_text:
            valid_to = _date_field(record, "valid_to", rule_id, errors)
            if valid_from is not None and valid_to is not None and valid_to < valid_from:
                errors.append(f"State financing row {rule_id} has valid_to before valid_from")

        notes = _field(record, "notes").lower()
        if not any(
            guardrail in notes for guardrail in ("not evidence", "does not by itself", "rule only")
        ):
            errors.append(f"State financing row {rule_id} must include interpretation guardrail")

        calculation_rule = _field(record, "calculation_rule").lower()
        if (
            transfer_type == "transferred_asset_financing"
            and "employer contribution" in calculation_rule
            and "not" not in calculation_rule
        ):
            errors.append(
                f"Transferred asset financing row {rule_id} cannot be an employer contribution"
            )
        if transfer_type == "specific_state_transfer" and state_role != "guarantor":
            errors.append(f"Specific State transfer row {rule_id} must use guarantor role")
        if transfer_type == "budget_appropriation_route" and status != "source_route_registered":
            errors.append(
                f"Budget appropriation route row {rule_id} must be source-route registered"
            )

    return errors


def _date_field(
    record: Any,
    column: str,
    rule_id: str,
    errors: list[str],
) -> date | None:
    value = _field(record, column)
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"State financing row {rule_id} has invalid {column}: {value}")
        return None


def _source_ids(source_registry_path: str | None) -> set[str] | None:
    if source_registry_path is None:
        return None
    sources = pd.read_csv(source_registry_path, dtype=str, keep_default_na=False)
    return set(sources["source_id"])


def _validate_cga_balance_decomposition(row: Any, row_number: int) -> list[str]:
    columns = {
        "balance_decomposition_residual",
        "pt_pension_fund_effect",
        "reported_global_balance",
        "reported_global_balance_ex_pt_fund",
    }
    present = {column for column in columns if _field(row, column)}
    if not present:
        return []
    if present != columns:
        missing = ", ".join(sorted(columns.difference(present)))
        return [f"CGA balance decomposition row {row_number} missing {missing}"]

    expected_residual = _numeric(row["reported_global_balance"], "reported_global_balance") - (
        _numeric(row["pt_pension_fund_effect"], "pt_pension_fund_effect")
        + _numeric(row["reported_global_balance_ex_pt_fund"], "reported_global_balance_ex_pt_fund")
    )
    recorded_residual = _numeric(
        row["balance_decomposition_residual"],
        "balance_decomposition_residual",
    )
    if not math.isclose(expected_residual, recorded_residual, rel_tol=0.0, abs_tol=0.11):
        return [f"CGA balance decomposition residual fails on row {row_number}"]
    return []


def _validate_cga_complete_identity(row: Any, row_number: int) -> list[str]:
    if _field(row, "status") != "complete":
        return []
    identity_columns = {
        "administration",
        "employee_quotations",
        "employer_contributions",
        "identity_residual",
        "investment_income",
        "other_benefits",
        "other_public_transfers",
        "pension_expenditure",
        "reported_global_balance",
        "state_budget_transfers",
    }
    if any(not _field(row, column) for column in identity_columns):
        return []
    result = reconcile_financing_identity(
        employee_contributions=_numeric(row["employee_quotations"], "employee_quotations"),
        employer_contributions=_numeric(row["employer_contributions"], "employer_contributions"),
        state_transfers=_numeric(row["state_budget_transfers"], "state_budget_transfers"),
        other_financing=(
            _numeric(row["other_public_transfers"], "other_public_transfers")
            + _numeric(row["investment_income"], "investment_income")
        ),
        pension_expenditure=_numeric(row["pension_expenditure"], "pension_expenditure"),
        administrative_expenditure=_numeric(row["administration"], "administration"),
        other_expenditure=_numeric(row["other_benefits"], "other_benefits"),
        change_in_financial_position=_numeric(
            row["reported_global_balance"],
            "reported_global_balance",
        ),
        tolerance=0.11,
    )
    recorded_residual = _numeric(row["identity_residual"], "identity_residual")
    if not math.isclose(result.residual, recorded_residual, rel_tol=0.0, abs_tol=0.11):
        return [f"CGA complete financing identity residual fails on row {row_number}"]
    return []


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
