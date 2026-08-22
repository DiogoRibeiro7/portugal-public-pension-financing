"""Validation of research registries and evidence contracts."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

from .accounting import (
    validate_cga_closed_scheme_decomposition,
    validate_cga_financing_ledger,
    validate_employee_remittance_audit,
    validate_employer_contribution_audit,
    validate_pension_flow_of_funds,
    validate_state_financing_rule_registry,
)
from .banking import (
    validate_bank_asset_liability_outputs,
    validate_bank_benefit_risk_distribution,
    validate_bank_esa_treatment_bridge,
    validate_bank_pension_cost_2012,
    validate_bank_pension_transfer_registry,
    validate_bank_special_regime_annual,
    validate_bank_transfer_debt_financing_effects,
    validate_bank_transfer_legal_coverage,
    validate_bank_worker_rgss_contributions,
    validate_bpn_2012_pension_transfer,
)
from .counterfactuals import (
    validate_counterfactual_financing_regimes,
    validate_fefss_return_inputs,
    validate_public_worker_liability_assumptions,
    validate_public_worker_reallocation,
    validate_public_worker_reallocation_bridge,
)
from .extraction import parse_accounting_number
from .legal import (
    validate_employer_perimeter_registry,
    validate_legal_contribution_registry,
    validate_rgss_rate_decomposition,
)
from .units import load_unit_registry

REQUIRED_EVIDENCE_FILES: tuple[str, ...] = (
    "analysis_protocol.csv",
    "analysis_protocol_hash.csv",
    "concept_registry.csv",
    "source_registry.csv",
    "source_acquisition_log.csv",
    "source_coverage_matrix.csv",
    "unit_registry.csv",
    "claim_registry.csv",
    "public_claim_registry.csv",
    "legal_contribution_registry.csv",
    "employer_perimeter_registry.csv",
    "rgss_rate_decomposition.csv",
    "state_financing_rule_registry.csv",
    "public_worker_liability_assumptions.csv",
    "bank_pension_transfer_registry.csv",
    "bank_special_regime_annual.csv",
    "extraction_audit.csv",
    "reconciliation_log.csv",
    "data_quality_registry.csv",
    "data_license_registry.csv",
    "counterfactual_registry.csv",
    "source_conflict_registry.csv",
    "uncertainty_registry.csv",
    "article_evidence.csv",
    "literature_map.csv",
    "figure_registry.csv",
    "table_registry.csv",
)

REQUIRED_FALSIFICATION_TESTS: frozenset[str] = frozenset(
    {
        "FALS_001",
        "FALS_002",
        "FALS_003",
        "FALS_004",
        "FALS_005",
        "FALS_006",
        "FALS_007",
        "FALS_008",
    }
)

REQUIRED_PUBLICATION_FIGURES: frozenset[str] = frozenset(
    {
        "FIG01",
        "FIG02",
        "FIG03",
        "FIG04",
        "FIG05",
        "FIG06",
        "FIG07",
        "FIG08",
        "FIG09",
        "FIG10",
        "FIG11",
    }
)

REQUIRED_RELEASE_READINESS_CHECKS: frozenset[str] = frozenset(
    {
        "REL_ARCHIVE_MANIFEST",
        "REL_DATA_GAPS_DOCUMENTED",
        "REL_FIGURE_COMPANIONS",
        "REL_GENERATED_EVIDENCE_POLICY",
        "REL_MANUSCRIPT_EVIDENCE_MATCH",
        "REL_NOTEBOOK_SEQUENCE",
        "REL_PINNED_ENVIRONMENT",
        "REL_QUALITY_GATE",
        "REL_SOURCE_HASHES",
    }
)

REQUIRED_SUBMISSION_PACKAGE_ITEMS: frozenset[str] = frozenset(
    {
        "SUB_ARCHIVE_MANIFEST",
        "SUB_ARTICLE_EVIDENCE",
        "SUB_AVAILABILITY",
        "SUB_MANUSCRIPT",
        "SUB_METHODS_APPENDIX",
        "SUB_RELEASE_AUDIT",
        "SUB_REPLICATION_GUIDE",
    }
)

REQUIRED_CLAIM_LANGUAGE_TERMS: frozenset[str] = frozenset(
    {
        "artificial",
        "debt",
        "deficit",
        "diverted",
        "harmful",
        "loss",
        "losses",
        "subsidy",
        "surplus",
        "sustainable",
        "underfunded",
    }
)

REQUIRED_ANALYSIS_PROTOCOL_HYPOTHESES: frozenset[str] = frozenset(
    {
        "H1",
        "H10",
        "H11",
        "H12",
        "H2",
        "H3",
        "H4",
        "H5",
        "H6",
        "H7",
        "H8",
        "H9",
    }
)

CONCEPT_REGISTRY_REQUIRED_COLUMNS: frozenset[str] = frozenset(
    {
        "concept_id",
        "source_label",
        "canonical_name",
        "concept_class",
        "definition",
        "valid_from",
        "valid_to",
        "institutional_perimeter",
        "accounting_basis",
        "source_id",
        "source_definition_status",
        "sign_convention",
        "internal_variable_names",
        "material_flow_columns",
        "ambiguous_label_guard",
        "notes",
    }
)

REQUIRED_CONCEPT_IDS: frozenset[str] = frozenset(
    {
        "ADMINISTRATION_COST",
        "ASSET_DRAWDOWN",
        "BANK_ASSET_TRANSFER",
        "CGA",
        "ECONOMIC_BENCHMARK_GAP",
        "EMPLOYEE_CONTRIBUTION",
        "EMPLOYER_CONTRIBUTION",
        "ESA_DEFICIT",
        "FINANCING_RESIDUAL",
        "INVESTMENT_INCOME",
        "LEGAL_GAP",
        "OTHER_BENEFIT_EXPENSE",
        "OTHER_FINANCING",
        "OTHER_PUBLIC_TRANSFER",
        "PENSION_EXPENDITURE",
        "PENSION_LIABILITY",
        "PREVIDENTIAL",
        "RGSS",
        "STATE_TRANSFER",
        "TIMING_ADJUSTMENT",
    }
)

CONCEPT_SOURCE_DEFINITION_STATUSES: frozenset[str] = frozenset(
    {
        "derived_accounting_bridge",
        "source_defined",
        "working_definition_requires_source",
    }
)

CONCEPT_SIGN_CONVENTIONS: frozenset[str] = frozenset(
    {
        "negative_expenditure_for_balance",
        "negative_for_deficit_increase",
        "not_applicable",
        "positive_asset_received_by_public_sector",
        "positive_financing_source",
        "positive_inflow_to_recipient",
        "positive_liability_stock",
        "positive_revenue_when_received",
        "signed_reconciliation_adjustment",
        "signed_reconciliation_residual",
    }
)

REQUIRED_MATERIAL_FLOW_MAPPINGS: frozenset[tuple[str, str]] = frozenset(
    {
        ("data/processed/bank_asset_liability_audit.csv", "assets_transferred_total"),
        ("data/processed/bank_asset_liability_audit.csv", "liability_pv_legal_4pct"),
        ("data/processed/bank_asset_liability_sensitivity.csv", "liability_pv"),
        ("data/processed/bank_asset_trace.csv", "transfer_value"),
        ("data/processed/bank_esa_treatment_bridge.csv", "deficit_effect_percent_gdp"),
        ("data/processed/bank_transfer_long_run.csv", "administrative_cost"),
        ("data/processed/bank_transfer_long_run.csv", "asset_drawdown"),
        ("data/processed/bank_transfer_long_run.csv", "attributable_investment_income"),
        ("data/processed/bank_transfer_long_run.csv", "other_financing"),
        ("data/processed/bank_transfer_long_run.csv", "pension_expenditure"),
        ("data/processed/bank_transfer_long_run.csv", "reconciliation_residual"),
        ("data/processed/bank_transfer_long_run.csv", "state_specific_transfer"),
        ("data/processed/cga_financing_ledger.csv", "administration"),
        ("data/processed/cga_financing_ledger.csv", "employee_quotations"),
        ("data/processed/cga_financing_ledger.csv", "employer_contributions"),
        ("data/processed/cga_financing_ledger.csv", "identity_residual"),
        ("data/processed/cga_financing_ledger.csv", "investment_income"),
        ("data/processed/cga_financing_ledger.csv", "other_benefits"),
        ("data/processed/cga_financing_ledger.csv", "other_public_transfers"),
        ("data/processed/cga_financing_ledger.csv", "pension_expenditure"),
        ("data/processed/cga_financing_ledger.csv", "state_budget_transfers"),
        ("data/processed/employee_remittance_audit.csv", "recorded_cga_worker_revenue"),
        ("data/processed/employee_remittance_audit.csv", "unexplained_remittance_gap"),
        ("data/processed/employer_contribution_audit.csv", "economic_benchmark_due"),
        ("data/processed/employer_contribution_audit.csv", "economic_benchmark_gap"),
        ("data/processed/employer_contribution_audit.csv", "legal_compliance_gap"),
        ("data/processed/employer_contribution_audit.csv", "legal_due"),
        ("data/processed/employer_contribution_audit.csv", "recorded_cga_employer_revenue"),
    }
)

AMBIGUOUS_ACCOUNTING_TERMS: frozenset[str] = frozenset(
    {
        "balance",
        "contribution",
        "deficit",
        "liability",
        "transfer",
    }
)

LITERATURE_MAP_REQUIRED_COLUMNS: frozenset[str] = frozenset(
    {
        "reference_id",
        "title",
        "year",
        "authors",
        "venue",
        "source_category",
        "topic",
        "research_question",
        "method",
        "data_period",
        "data_source",
        "main_finding",
        "relation_to_paper",
        "novelty_role",
        "inclusion_decision",
        "search_database",
        "search_query",
        "search_date",
        "source_url",
        "notes",
    }
)

LITERATURE_SOURCE_CATEGORIES: frozenset[str] = frozenset(
    {
        "academic_literature",
        "institutional_review",
        "technical_accounting_source",
    }
)

LITERATURE_INCLUSION_DECISIONS: frozenset[str] = frozenset(
    {
        "excluded_not_relevant",
        "excluded_no_accessible_metadata",
        "included_context",
        "included_nearest_neighbor",
    }
)

SOURCE_COVERAGE_REQUIRED_COLUMNS: frozenset[str] = frozenset(
    {
        "variable_id",
        "year",
        "source_id",
        "coverage_status",
        "format",
        "granularity",
        "definition_break",
        "revision_status",
        "notes",
    }
)

SOURCE_COVERAGE_CORE_VARIABLES: frozenset[str] = frozenset(
    {
        "bank_asset_liability_transfer_schedules",
        "bank_pension_transfer_legal",
        "cga_employee_employer_revenue_split",
        "cga_reports_accounts",
        "cga_subscriber_pensioner_counts",
        "cge_public_accounts",
        "esa_pension_transfer_treatment",
        "legal_contribution_rules",
        "public_employment_counts",
        "public_worker_cohort_inputs",
        "social_security_accounts",
        "state_budget_documents",
    }
)

SOURCE_COVERAGE_STATUSES: frozenset[str] = frozenset(
    {
        "definition-break",
        "not-applicable",
        "observed",
        "revision-conflict",
        "unavailable",
    }
)

SOURCE_COVERAGE_YEARS: frozenset[int] = frozenset(range(1977, 2026))

SOURCE_ACQUISITION_LOG_REQUIRED_COLUMNS: frozenset[str] = frozenset(
    {
        "source_id",
        "attempted_url",
        "retrieval_date",
        "raw_path",
        "sha256",
        "status",
        "notes",
    }
)

SOURCE_ACQUISITION_STATUSES: frozenset[str] = frozenset(
    {
        "acquired",
        "failed",
        "shell_html_not_evidence",
    }
)

EXTRACTION_AUDIT_REQUIRED_COLUMNS: frozenset[str] = frozenset(
    {
        "source_id",
        "page",
        "table_title",
        "row_label",
        "column_label",
        "original_text",
        "parsed_value",
        "unit",
        "extraction_method",
        "validation_method",
        "qa_tier",
        "secondary_check",
        "parsing_warning",
        "status",
        "notes",
    }
)

EXTRACTION_AUDIT_STATUSES: frozenset[str] = frozenset(
    {
        "extracted",
        "reconciled",
        "reconciled_rounding",
        "replicated_approximation",
    }
)

EXTRACTION_QA_TIERS: frozenset[str] = frozenset({"high_impact", "routine"})

NON_NUMERIC_EXTRACTION_UNITS: frozenset[str] = frozenset({"legal_scope", "qualitative"})

UNIT_REGISTRY_REQUIRED_COLUMNS: frozenset[str] = frozenset(
    {
        "unit_id",
        "currency",
        "scale",
        "price_basis",
        "base_year",
        "flow_or_stock",
        "accounting_basis",
        "conversion_rule",
        "valid_from",
        "valid_to",
        "canonical_unit",
        "join_family",
        "notes",
    }
)

UNIT_REGISTRY_REQUIRED_UNITS: frozenset[str] = frozenset(
    {
        "EUR_million",
        "EUR_million_and_percent_GDP",
        "PTE_million",
        "count",
        "date",
        "mixed",
        "not_applicable",
        "percent",
        "percent_GDP",
        "rate",
        "share_of_assets",
        "share_of_provisional_value",
        "text",
        "workers",
    }
)

UNIT_REGISTRY_CONVERSION_RULES: frozenset[str] = frozenset(
    {
        "divide_by_100_for_rate",
        "fixed_escudo_euro_200_482",
        "none",
        "split_before_join",
    }
)

SOURCE_CONFLICT_REQUIRED_COLUMNS: frozenset[str] = frozenset(
    {
        "conflict_id",
        "concept_id",
        "period",
        "source_id_a",
        "value_a",
        "source_id_b",
        "value_b",
        "unit",
        "difference_type",
        "tolerance_rule",
        "materiality_rule",
        "resolution",
        "status",
        "uncertainty_id",
        "notes",
    }
)

SOURCE_CONFLICT_DIFFERENCE_TYPES: frozenset[str] = frozenset(
    {
        "accounting_basis",
        "perimeter_and_accounting_item",
        "rounding",
        "rounding_and_component_split",
        "rounding_approximation",
        "timing",
        "transcription",
        "unresolved",
    }
)

SOURCE_CONFLICT_STATUSES: frozenset[str] = frozenset(
    {
        "documented_not_same_quantity",
        "reconciled_approximation",
        "reconciled_by_estimand",
        "reconciled_rounding",
        "unresolved_range",
    }
)

UNCERTAINTY_REGISTRY_REQUIRED_COLUMNS: frozenset[str] = frozenset(
    {
        "estimate_id",
        "source_or_model",
        "lower",
        "central",
        "upper",
        "unit",
        "uncertainty_reason",
        "method",
        "status",
    }
)

UNCERTAINTY_STATUSES: frozenset[str] = frozenset(
    {
        "reconciled_bounded",
        "reconciled_rounding",
        "unresolved_range",
    }
)

DATA_LICENSE_REQUIRED_COLUMNS: frozenset[str] = frozenset(
    {
        "source_id",
        "access_status",
        "redistribution_status",
        "license_or_terms",
        "retrieval_method",
        "archival_reference",
        "clean_room_instruction",
        "repository_action",
        "notes",
    }
)

DATA_LICENSE_ACCESS_STATUSES: frozenset[str] = frozenset(
    {
        "acquired_public_download",
        "registered_public_url",
        "retrieval_failed_public_url",
    }
)

DATA_LICENSE_REDISTRIBUTION_STATUSES: frozenset[str] = frozenset(
    {
        "allowed_with_attribution",
        "permission_unclear_do_not_redistribute",
        "not_acquired_no_redistribution",
    }
)

ARTICLE_EVIDENCE_REQUIRED_CLAIM_TYPES: frozenset[str] = frozenset(
    {
        "published_quantitative_claim",
        "published_account_extract",
        "legal_quantitative_fact",
        "accounting_treatment",
    }
)

ARTICLE_EVIDENCE_BLOCKING_STATUSES: frozenset[str] = frozenset(
    {
        "to_replicate",
        "unresolved",
    }
)

TEXT_MANIFEST_SUFFIXES: frozenset[str] = frozenset(
    {
        ".cff",
        ".csv",
        ".gitignore",
        ".json",
        ".md",
        ".py",
        ".sha256",
        ".tex",
        ".toml",
        ".txt",
        ".yml",
        ".yaml",
    }
)
TEXT_MANIFEST_NAMES: frozenset[str] = frozenset({"Makefile"})


def validate_evidence_directory(evidence_dir: Path) -> list[str]:
    """Return validation errors for the repository evidence directory."""
    if not isinstance(evidence_dir, Path):
        raise TypeError("evidence_dir must be pathlib.Path")
    errors: list[str] = []
    for filename in REQUIRED_EVIDENCE_FILES:
        path = evidence_dir / filename
        if not path.is_file():
            errors.append(f"Missing evidence file: {filename}")
            continue
        try:
            pd.read_csv(path)
        except Exception as exc:  # pragma: no cover - defensive parsing boundary
            errors.append(f"Unreadable CSV {filename}: {exc}")
    if (evidence_dir / "source_registry.csv").is_file():
        errors.extend(
            validate_source_registry(evidence_dir / "source_registry.csv", evidence_dir.parent)
        )
    public_claim_registry = evidence_dir / "public_claim_registry.csv"
    working_group_replication = (
        evidence_dir.parent / "data" / "processed" / "working_group_2026_replication.csv"
    )
    if public_claim_registry.is_file() and working_group_replication.is_file():
        errors.extend(
            validate_public_claim_registry(public_claim_registry, working_group_replication)
        )
    combined_balance_replication = (
        evidence_dir.parent / "data" / "processed" / "combined_balance_replication_2026.csv"
    )
    combined_balance_bridge = (
        evidence_dir.parent / "data" / "processed" / "combined_balance_component_bridge_2026.csv"
    )
    if combined_balance_replication.is_file() and combined_balance_bridge.is_file():
        errors.extend(
            validate_combined_balance_replication(
                combined_balance_replication,
                combined_balance_bridge,
            )
        )
    joint_balance_definitions = (
        evidence_dir.parent / "data" / "processed" / "joint_balance_definitions.csv"
    )
    joint_balance_rules = (
        evidence_dir.parent / "data" / "processed" / "joint_balance_definition_rules.csv"
    )
    if joint_balance_definitions.is_file() and joint_balance_rules.is_file():
        errors.extend(
            validate_joint_balance_definitions(joint_balance_definitions, joint_balance_rules)
        )
    if (evidence_dir / "data_license_registry.csv").is_file() and (
        evidence_dir / "source_registry.csv"
    ).is_file():
        errors.extend(
            validate_data_license_registry(
                evidence_dir / "data_license_registry.csv",
                evidence_dir / "source_registry.csv",
            )
        )
    if (evidence_dir / "unit_registry.csv").is_file():
        errors.extend(
            validate_unit_registry(evidence_dir / "unit_registry.csv", evidence_dir.parent)
        )
    if (evidence_dir / "source_conflict_registry.csv").is_file() and (
        evidence_dir / "uncertainty_registry.csv"
    ).is_file():
        errors.extend(
            validate_conflict_and_uncertainty_registries(
                evidence_dir / "source_conflict_registry.csv",
                evidence_dir / "uncertainty_registry.csv",
                evidence_dir / "source_registry.csv",
                evidence_dir / "concept_registry.csv",
                evidence_dir / "unit_registry.csv",
            )
        )
    if (evidence_dir / "source_acquisition_log.csv").is_file():
        errors.extend(
            validate_source_acquisition_log(
                evidence_dir / "source_acquisition_log.csv",
                evidence_dir / "source_registry.csv",
                evidence_dir.parent,
            )
        )
    if (evidence_dir / "extraction_audit.csv").is_file():
        errors.extend(
            validate_extraction_audit(
                evidence_dir / "extraction_audit.csv",
                evidence_dir / "source_registry.csv",
            )
        )
    if (evidence_dir / "source_coverage_matrix.csv").is_file():
        errors.extend(
            validate_source_coverage_matrix(
                evidence_dir / "source_coverage_matrix.csv",
                evidence_dir / "source_registry.csv",
                evidence_dir.parent / "docs" / "historical_data_gap_map.md",
            )
        )
    if (evidence_dir / "concept_registry.csv").is_file():
        errors.extend(
            validate_concept_registry(evidence_dir / "concept_registry.csv", evidence_dir.parent)
        )
    if (evidence_dir / "literature_map.csv").is_file():
        errors.extend(
            validate_literature_map(
                evidence_dir / "literature_map.csv",
                evidence_dir.parent / "docs" / "literature_search_protocol.md",
                evidence_dir.parent / "docs" / "related_work_synthesis.md",
            )
        )
    if (evidence_dir / "analysis_protocol.csv").is_file():
        errors.extend(
            validate_analysis_protocol(
                evidence_dir / "analysis_protocol.csv",
                evidence_dir / "analysis_protocol_hash.csv",
            )
        )
    if (evidence_dir / "legal_contribution_registry.csv").is_file():
        errors.extend(
            validate_legal_contribution_registry(
                str(evidence_dir / "legal_contribution_registry.csv"),
                str(evidence_dir / "source_registry.csv"),
            )
        )
    if (evidence_dir / "employer_perimeter_registry.csv").is_file():
        errors.extend(
            validate_employer_perimeter_registry(
                str(evidence_dir / "employer_perimeter_registry.csv"),
                str(evidence_dir / "source_registry.csv"),
                str(evidence_dir / "legal_contribution_registry.csv"),
            )
        )
    if (evidence_dir / "rgss_rate_decomposition.csv").is_file():
        errors.extend(
            validate_rgss_rate_decomposition(
                str(evidence_dir / "rgss_rate_decomposition.csv"),
                str(evidence_dir / "source_registry.csv"),
            )
        )
    if (evidence_dir / "bank_pension_transfer_registry.csv").is_file():
        errors.extend(
            validate_bank_pension_transfer_registry(
                str(evidence_dir / "bank_pension_transfer_registry.csv")
            )
        )
    bank_transfer_legal_coverage = (
        evidence_dir.parent / "data" / "processed" / "bank_transfer_legal_coverage.csv"
    )
    if (
        bank_transfer_legal_coverage.is_file()
        and (evidence_dir / "bank_pension_transfer_registry.csv").is_file()
    ):
        errors.extend(
            validate_bank_transfer_legal_coverage(
                str(bank_transfer_legal_coverage),
                str(evidence_dir / "bank_pension_transfer_registry.csv"),
            )
        )
    bank_worker_contributions = (
        evidence_dir.parent / "data" / "processed" / "bank_worker_rgss_contributions.csv"
    )
    bank_worker_mapping = (
        evidence_dir.parent / "data" / "processed" / "bank_worker_legal_population_mapping.csv"
    )
    if bank_worker_contributions.is_file() and bank_worker_mapping.is_file():
        errors.extend(
            validate_bank_worker_rgss_contributions(
                str(bank_worker_contributions),
                str(bank_worker_mapping),
            )
        )
    if (evidence_dir / "bank_special_regime_annual.csv").is_file():
        errors.extend(
            validate_bank_special_regime_annual(
                str(evidence_dir / "bank_special_regime_annual.csv")
            )
        )
    if (evidence_dir / "state_financing_rule_registry.csv").is_file():
        errors.extend(
            validate_state_financing_rule_registry(
                str(evidence_dir / "state_financing_rule_registry.csv"),
                str(evidence_dir / "source_registry.csv"),
            )
        )
    bank_asset_liability = (
        evidence_dir.parent / "data" / "processed" / "bank_asset_liability_audit.csv"
    )
    bank_asset_trace = evidence_dir.parent / "data" / "processed" / "bank_asset_trace.csv"
    bank_sensitivity = (
        evidence_dir.parent / "data" / "processed" / "bank_asset_liability_sensitivity.csv"
    )
    if bank_asset_liability.is_file() and bank_asset_trace.is_file() and bank_sensitivity.is_file():
        errors.extend(
            validate_bank_asset_liability_outputs(
                str(bank_asset_liability),
                str(bank_asset_trace),
                str(bank_sensitivity),
            )
        )
    bank_benefit_risk = (
        evidence_dir.parent / "data" / "processed" / "bank_benefit_risk_distribution.csv"
    )
    if bank_benefit_risk.is_file():
        errors.extend(validate_bank_benefit_risk_distribution(str(bank_benefit_risk)))
    bank_esa_bridge = evidence_dir.parent / "data" / "processed" / "bank_esa_treatment_bridge.csv"
    if bank_esa_bridge.is_file():
        errors.extend(validate_bank_esa_treatment_bridge(str(bank_esa_bridge)))
    bank_pension_cost = evidence_dir.parent / "data" / "processed" / "bank_pension_cost_2012.csv"
    if bank_pension_cost.is_file():
        errors.extend(validate_bank_pension_cost_2012(str(bank_pension_cost)))
    bank_debt_financing = (
        evidence_dir.parent / "data" / "processed" / "bank_transfer_debt_financing_effects.csv"
    )
    if bank_debt_financing.is_file():
        errors.extend(validate_bank_transfer_debt_financing_effects(str(bank_debt_financing)))
    bpn_transfer = evidence_dir.parent / "data" / "processed" / "bpn_2012_pension_transfer.csv"
    if bpn_transfer.is_file():
        errors.extend(validate_bpn_2012_pension_transfer(str(bpn_transfer)))
    cga_ledger = evidence_dir.parent / "data" / "processed" / "cga_financing_ledger.csv"
    if cga_ledger.is_file():
        errors.extend(
            validate_cga_financing_ledger(
                str(cga_ledger),
                str(evidence_dir / "source_registry.csv"),
            )
        )
    cga_closure = evidence_dir.parent / "data" / "processed" / "cga_closed_scheme_decomposition.csv"
    if cga_closure.is_file():
        errors.extend(validate_cga_closed_scheme_decomposition(str(cga_closure)))
    pension_flow_matrix = (
        evidence_dir.parent / "data" / "processed" / "pension_flow_of_funds_long.csv"
    )
    if pension_flow_matrix.is_file():
        errors.extend(validate_pension_flow_of_funds(str(pension_flow_matrix)))
    employee_remittance = (
        evidence_dir.parent / "data" / "processed" / "employee_remittance_audit.csv"
    )
    if employee_remittance.is_file():
        errors.extend(
            validate_employee_remittance_audit(
                str(employee_remittance),
                str(evidence_dir / "source_registry.csv"),
            )
        )
    employer_contribution = (
        evidence_dir.parent / "data" / "processed" / "employer_contribution_audit.csv"
    )
    if employer_contribution.is_file():
        errors.extend(
            validate_employer_contribution_audit(
                str(employer_contribution),
                str(evidence_dir / "source_registry.csv"),
            )
        )
    public_worker_cohorts = (
        evidence_dir.parent / "data" / "processed" / "public_worker_rgss_cohorts.csv"
    )
    public_worker_contributions = (
        evidence_dir.parent
        / "data"
        / "processed"
        / "public_worker_rgss_contributions_2006_2025.csv"
    )
    if public_worker_cohorts.is_file() and public_worker_contributions.is_file():
        errors.extend(
            validate_public_worker_reallocation(
                str(public_worker_cohorts),
                str(public_worker_contributions),
            )
        )
    public_worker_bridge = (
        evidence_dir.parent / "data" / "processed" / "public_worker_reallocation_bridge.csv"
    )
    if public_worker_bridge.is_file():
        errors.extend(
            validate_public_worker_reallocation_bridge(
                str(public_worker_bridge),
                str(evidence_dir / "source_registry.csv"),
            )
        )
    public_worker_liability_assumptions = evidence_dir / "public_worker_liability_assumptions.csv"
    if public_worker_liability_assumptions.is_file():
        errors.extend(
            validate_public_worker_liability_assumptions(
                str(public_worker_liability_assumptions),
                str(evidence_dir / "source_registry.csv"),
            )
        )
    counterfactual_regimes = (
        evidence_dir.parent / "data" / "processed" / "counterfactual_financing_regimes.csv"
    )
    if counterfactual_regimes.is_file():
        errors.extend(
            validate_counterfactual_financing_regimes(
                str(evidence_dir / "counterfactual_registry.csv"),
                str(counterfactual_regimes),
            )
        )
    fefss_returns = evidence_dir.parent / "data" / "processed" / "fefss_returns.csv"
    fefss_counterfactual = (
        evidence_dir.parent / "data" / "processed" / "public_worker_fefss_counterfactual.csv"
    )
    fefss_sensitivity = (
        evidence_dir.parent / "data" / "processed" / "public_worker_fefss_sensitivity.csv"
    )
    if fefss_returns.is_file() and fefss_counterfactual.is_file():
        errors.extend(
            validate_fefss_return_inputs(
                str(fefss_returns),
                str(fefss_counterfactual),
                str(evidence_dir / "source_registry.csv"),
                str(fefss_sensitivity) if fefss_sensitivity.is_file() else None,
            )
        )
    falsification_review = evidence_dir.parent / "data" / "processed" / "falsification_review.csv"
    if falsification_review.is_file():
        errors.extend(validate_falsification_review(falsification_review))
    article_evidence = evidence_dir / "article_evidence.csv"
    internal_replication = (
        evidence_dir.parent / "data" / "processed" / "internal_replication_review.csv"
    )
    if internal_replication.is_file() and article_evidence.is_file():
        errors.extend(validate_internal_replication_review(internal_replication, article_evidence))
    release_readiness = (
        evidence_dir.parent / "data" / "processed" / "release_reproducibility_audit.csv"
    )
    if release_readiness.is_file():
        errors.extend(
            validate_release_reproducibility_audit(release_readiness, evidence_dir.parent)
        )
    submission_package = (
        evidence_dir.parent / "data" / "processed" / "submission_package_manifest.csv"
    )
    if submission_package.is_file():
        errors.extend(validate_submission_package(submission_package, evidence_dir.parent))
    figure_registry = evidence_dir.parent / "paper" / "figures" / "figure_registry.csv"
    table_registry = evidence_dir.parent / "paper" / "tables" / "table_registry.csv"
    if figure_registry.is_file() and table_registry.is_file():
        errors.extend(
            validate_publication_artifacts(figure_registry, table_registry, evidence_dir.parent)
        )
    article_figure_registry = evidence_dir / "figure_registry.csv"
    article_table_registry = evidence_dir / "table_registry.csv"
    if (
        article_evidence.is_file()
        and article_figure_registry.is_file()
        and article_table_registry.is_file()
    ):
        errors.extend(
            validate_article_evidence(
                article_evidence,
                evidence_dir / "claim_registry.csv",
                article_figure_registry,
                article_table_registry,
                evidence_dir.parent,
            )
        )
    manuscript = evidence_dir.parent / "paper" / "manuscript.tex"
    if manuscript.is_file() and article_evidence.is_file():
        errors.extend(validate_manuscript_draft(manuscript, article_evidence))
    language_audit = (
        evidence_dir.parent / "data" / "processed" / "manuscript_claim_language_audit.csv"
    )
    if language_audit.is_file() and manuscript.is_file():
        errors.extend(validate_claim_language_audit(language_audit, manuscript))
    return errors


def validate_conflict_and_uncertainty_registries(
    conflict_path: Path,
    uncertainty_path: Path,
    source_registry_path: Path,
    concept_registry_path: Path,
    unit_registry_path: Path,
) -> list[str]:
    """Return validation errors for conflict and uncertainty registries."""
    for path, name in (
        (conflict_path, "conflict_path"),
        (uncertainty_path, "uncertainty_path"),
        (source_registry_path, "source_registry_path"),
        (concept_registry_path, "concept_registry_path"),
        (unit_registry_path, "unit_registry_path"),
    ):
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")

    conflicts = pd.read_csv(conflict_path, dtype=str, keep_default_na=False)
    uncertainty = pd.read_csv(uncertainty_path, dtype=str, keep_default_na=False)
    missing_conflict_columns = sorted(
        SOURCE_CONFLICT_REQUIRED_COLUMNS.difference(conflicts.columns)
    )
    if missing_conflict_columns:
        return [f"Source conflict registry missing columns: {', '.join(missing_conflict_columns)}"]
    missing_uncertainty_columns = sorted(
        UNCERTAINTY_REGISTRY_REQUIRED_COLUMNS.difference(uncertainty.columns)
    )
    if missing_uncertainty_columns:
        return [f"Uncertainty registry missing columns: {', '.join(missing_uncertainty_columns)}"]

    sources = pd.read_csv(source_registry_path, dtype=str, keep_default_na=False)
    concepts = pd.read_csv(concept_registry_path, dtype=str, keep_default_na=False)
    units = pd.read_csv(unit_registry_path, dtype=str, keep_default_na=False)
    source_ids = set(sources["source_id"])
    concept_ids = set(concepts["concept_id"])
    unit_ids = set(units["unit_id"])
    uncertainty_ids = set(uncertainty["estimate_id"])

    errors: list[str] = []
    duplicate_conflicts = sorted(
        conflicts.loc[conflicts["conflict_id"].duplicated(), "conflict_id"].dropna().unique()
    )
    for conflict_id in duplicate_conflicts:
        errors.append(f"Duplicate source conflict row: {conflict_id}")

    duplicate_uncertainty = sorted(
        uncertainty.loc[uncertainty["estimate_id"].duplicated(), "estimate_id"].dropna().unique()
    )
    for estimate_id in duplicate_uncertainty:
        errors.append(f"Duplicate uncertainty row: {estimate_id}")

    if len(conflicts) < 5:
        errors.append("Source conflict registry must contain at least 5 bounded conflict rows")
    if len(uncertainty) < 5:
        errors.append("Uncertainty registry must contain at least 5 bounded uncertainty rows")

    for row in conflicts.to_dict("records"):
        conflict_id = row["conflict_id"].strip()
        if not conflict_id:
            errors.append("Source conflict registry contains a row with empty conflict_id")
            continue
        for column in SOURCE_CONFLICT_REQUIRED_COLUMNS:
            if not row[column].strip():
                errors.append(f"Source conflict row {conflict_id} has empty {column}")
        if row["concept_id"] not in concept_ids:
            errors.append(f"Source conflict {conflict_id} references unknown concept_id")
        for source_id in (row["source_id_a"], row["source_id_b"]):
            if source_id not in source_ids:
                errors.append(
                    f"Source conflict {conflict_id} references unknown source_id: {source_id}"
                )
        if row["unit"] not in unit_ids:
            errors.append(f"Source conflict {conflict_id} references unknown unit")
        if row["difference_type"] not in SOURCE_CONFLICT_DIFFERENCE_TYPES:
            errors.append(
                f"Source conflict {conflict_id} has invalid difference_type: "
                f"{row['difference_type']}"
            )
        if row["status"] not in SOURCE_CONFLICT_STATUSES:
            errors.append(f"Source conflict {conflict_id} has invalid status: {row['status']}")
        if row["uncertainty_id"] not in uncertainty_ids:
            errors.append(f"Source conflict {conflict_id} references unknown uncertainty_id")
        if row["status"] == "unresolved_range" and "range" not in row["resolution"].lower():
            errors.append(f"Unresolved conflict {conflict_id} must document a range")
        try:
            float(row["value_a"])
            float(row["value_b"])
        except ValueError:
            errors.append(f"Source conflict {conflict_id} has non-numeric conflict value")

    for row in uncertainty.to_dict("records"):
        estimate_id = row["estimate_id"].strip()
        if not estimate_id:
            errors.append("Uncertainty registry contains a row with empty estimate_id")
            continue
        for column in UNCERTAINTY_REGISTRY_REQUIRED_COLUMNS.difference({"central"}):
            if not row[column].strip():
                errors.append(f"Uncertainty row {estimate_id} has empty {column}")
        if row["unit"] not in unit_ids:
            errors.append(f"Uncertainty row {estimate_id} references unknown unit")
        if row["status"] not in UNCERTAINTY_STATUSES:
            errors.append(f"Uncertainty row {estimate_id} has invalid status: {row['status']}")
        try:
            lower = float(row["lower"])
            upper = float(row["upper"])
            central = float(row["central"]) if row["central"].strip() else None
        except ValueError:
            errors.append(f"Uncertainty row {estimate_id} has non-numeric bounds")
            continue
        if lower > upper:
            errors.append(f"Uncertainty row {estimate_id} lower bound exceeds upper bound")
        if central is not None and not lower <= central <= upper:
            errors.append(f"Uncertainty row {estimate_id} central value outside bounds")
        if row["status"] == "unresolved_range" and row["central"].strip():
            errors.append(f"Unresolved uncertainty row {estimate_id} must leave central empty")

    return errors


def validate_unit_registry(registry_path: Path, root: Path) -> list[str]:
    """Return validation errors for unit/currency/price-basis metadata."""
    if not isinstance(registry_path, Path):
        raise TypeError("registry_path must be pathlib.Path")
    if not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")

    registry = pd.read_csv(registry_path, dtype=str, keep_default_na=False)
    missing_columns = sorted(UNIT_REGISTRY_REQUIRED_COLUMNS.difference(registry.columns))
    if missing_columns:
        return [f"Unit registry missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    unit_ids = set(registry["unit_id"])
    for unit_id in sorted(UNIT_REGISTRY_REQUIRED_UNITS.difference(unit_ids)):
        errors.append(f"Missing required unit registry row: {unit_id}")

    duplicate_ids = sorted(
        registry.loc[registry["unit_id"].duplicated(), "unit_id"].dropna().unique()
    )
    for unit_id in duplicate_ids:
        errors.append(f"Duplicate unit registry row: {unit_id}")

    for row in registry.to_dict("records"):
        unit_id = row["unit_id"].strip()
        if not unit_id:
            errors.append("Unit registry contains a row with empty unit_id")
            continue
        for column in (
            "currency",
            "scale",
            "price_basis",
            "flow_or_stock",
            "accounting_basis",
            "conversion_rule",
            "valid_from",
            "canonical_unit",
            "join_family",
            "notes",
        ):
            if not row[column].strip():
                errors.append(f"Unit registry row {unit_id} has empty {column}")
        if row["conversion_rule"] not in UNIT_REGISTRY_CONVERSION_RULES:
            errors.append(
                f"Unit registry row {unit_id} has invalid conversion_rule: {row['conversion_rule']}"
            )
        if row["conversion_rule"] == "fixed_escudo_euro_200_482" and (
            row["currency"] != "PTE" or row["canonical_unit"] != "EUR_million"
        ):
            errors.append(f"Escudo conversion row {unit_id} has invalid canonical metadata")

    try:
        load_unit_registry(registry_path)
    except TypeError as exc:
        errors.append(f"Unit registry cannot load definitions: {exc}")

    observed_units: set[str] = set()
    for directory in (root / "data" / "processed", root / "evidence"):
        if not directory.is_dir():
            continue
        for csv_path in directory.glob("*.csv"):
            table = pd.read_csv(csv_path, dtype=str, keep_default_na=False, nrows=5000)
            if "unit" in table.columns:
                observed_units.update(value for value in table["unit"].unique() if value)
    missing_observed_units = observed_units.difference(unit_ids).difference(
        NON_NUMERIC_EXTRACTION_UNITS
    )
    for unit in sorted(missing_observed_units):
        errors.append(f"Observed CSV unit is missing from unit registry: {unit}")

    return errors


def _extraction_value(
    audit: pd.DataFrame,
    source_id: str,
    page: str,
    row_label: str,
    column_label: str,
) -> float | None:
    matches = audit[
        (audit["source_id"] == source_id)
        & (audit["page"] == page)
        & (audit["row_label"] == row_label)
        & (audit["column_label"] == column_label)
    ]
    if len(matches) != 1:
        return None
    value = matches.iloc[0]["parsed_value"]
    if not value:
        return None
    return float(value)


def validate_extraction_audit(audit_path: Path, source_registry_path: Path) -> list[str]:
    """Return validation errors for PDF/table extraction audit rows."""
    if not isinstance(audit_path, Path):
        raise TypeError("audit_path must be pathlib.Path")
    if not isinstance(source_registry_path, Path):
        raise TypeError("source_registry_path must be pathlib.Path")

    audit = pd.read_csv(audit_path, dtype=str, keep_default_na=False)
    missing_columns = sorted(EXTRACTION_AUDIT_REQUIRED_COLUMNS.difference(audit.columns))
    if missing_columns:
        return [f"Extraction audit missing columns: {', '.join(missing_columns)}"]

    source_ids: set[str] = set()
    if source_registry_path.is_file():
        source_registry = pd.read_csv(source_registry_path, dtype=str, keep_default_na=False)
        if "source_id" in source_registry.columns:
            source_ids = set(source_registry["source_id"])

    errors: list[str] = []
    duplicate_rows = audit[
        audit.duplicated(
            subset=["source_id", "page", "table_title", "row_label", "column_label"],
            keep=False,
        )
    ]
    for row in duplicate_rows.to_dict("records"):
        errors.append(
            "Duplicate extraction audit row: "
            f"{row['source_id']} {row['page']} {row['row_label']} {row['column_label']}"
        )

    high_impact_count = 0
    for row_number, row in enumerate(audit.to_dict("records"), start=2):
        locator = f"{row['source_id']} page {row['page']} {row['row_label']} {row['column_label']}"
        for column in (
            "source_id",
            "page",
            "table_title",
            "row_label",
            "column_label",
            "original_text",
            "unit",
            "extraction_method",
            "validation_method",
            "qa_tier",
            "secondary_check",
            "parsing_warning",
            "status",
            "notes",
        ):
            if not row[column].strip():
                errors.append(f"Extraction audit row {row_number} has empty {column}")

        source_id = row["source_id"].strip()
        if source_ids and source_id not in source_ids:
            errors.append(f"Extraction audit references unknown source_id: {source_id}")

        status = row["status"].strip()
        if status not in EXTRACTION_AUDIT_STATUSES:
            errors.append(f"Extraction audit row {locator} has invalid status: {status}")

        qa_tier = row["qa_tier"].strip()
        if qa_tier not in EXTRACTION_QA_TIERS:
            errors.append(f"Extraction audit row {locator} has invalid qa_tier: {qa_tier}")
        if qa_tier == "high_impact":
            high_impact_count += 1
            if row["secondary_check"].strip() in {"", "not_required", "none"}:
                errors.append(f"High-impact extraction row lacks secondary check: {locator}")

        if (
            "ocr" in row["extraction_method"].lower()
            and "unchecked" in row["validation_method"].lower()
        ):
            errors.append(f"Extraction audit row uses unchecked OCR: {locator}")

        parsed_value = row["parsed_value"].strip()
        unit = row["unit"].strip()
        if unit not in NON_NUMERIC_EXTRACTION_UNITS:
            if not parsed_value:
                errors.append(f"Numeric extraction row lacks parsed_value: {locator}")
            else:
                try:
                    parsed_numeric = float(parsed_value)
                    source_numbers = [
                        value
                        for value in re.findall(r"[-+]?\d+(?:[.,]\d+)?", row["original_text"])
                        if value.lstrip("+-").split(",", maxsplit=1)[0].split(".", maxsplit=1)[0]
                        not in {str(year) for year in range(1900, 2101)}
                    ]
                    source_numeric = (
                        parse_accounting_number(row["original_text"])
                        if len(source_numbers) == 1
                        else None
                    )
                except ValueError:
                    source_numeric = None
                expected_values = {parsed_numeric}
                if source_numeric is not None:
                    expected_values = {source_numeric}
                    if unit == "EUR_million" and abs(source_numeric) >= 1_000_000:
                        expected_values.add(source_numeric / 1_000_000)
                    if unit == "EUR_million" and "thousand" in row["original_text"].lower():
                        expected_values.add(source_numeric / 1_000)
                    if unit == "rate" or unit.startswith("share_"):
                        expected_values.add(source_numeric / 100)
                if source_numeric is not None and all(
                    abs(parsed_numeric - expected) > 1e-9 for expected in expected_values
                ):
                    errors.append(f"Parsed value does not match original text: {locator}")
            if row["parsing_warning"].strip() != "none":
                errors.append(f"Numeric extraction row carries parsing warning: {locator}")
        elif parsed_value and row["parsing_warning"].strip() != "none":
            errors.append(f"Non-numeric extraction row carries parsing warning: {locator}")

    if high_impact_count < 8:
        errors.append("Extraction audit must identify at least 8 high-impact rows")

    cga_balance = _extraction_value(audit, "DGO_CGE_2011", "159", "CGA", "Saldo Global 2011")
    pt_fund = _extraction_value(
        audit,
        "DGO_CGE_2011",
        "159",
        "Fundo de Pensões da PT",
        "Saldo Global 2011",
    )
    cga_without_pt = _extraction_value(
        audit,
        "DGO_CGE_2011",
        "159",
        "CGA sem Fundo de Pensões da PT",
        "Saldo Global 2011",
    )
    if cga_balance is not None and pt_fund is not None and cga_without_pt is not None:
        residual = cga_balance - pt_fund - cga_without_pt
        if abs(residual) > 0.2:
            errors.append("CGA/PT fund extraction identity exceeds rounding tolerance")

    tc_revenue = _extraction_value(
        audit,
        "TC_AEO_2013_SS_2012",
        "19",
        "banking substitute-regime pensions",
        "current-transfer financing",
    )
    tc_expenditure = _extraction_value(
        audit,
        "TC_AEO_2013_SS_2012",
        "20",
        "banking substitute-regime pensions",
        "current-transfer expenditure",
    )
    if tc_revenue is not None and tc_expenditure is not None and abs(tc_revenue - tc_expenditure):
        errors.append("Banking substitute-regime extraction revenue/expenditure mismatch")

    return errors


def validate_source_acquisition_log(
    log_path: Path,
    source_registry_path: Path,
    root: Path,
) -> list[str]:
    """Return validation errors for raw-source acquisition attempts."""
    if not isinstance(log_path, Path):
        raise TypeError("log_path must be pathlib.Path")
    if not isinstance(source_registry_path, Path):
        raise TypeError("source_registry_path must be pathlib.Path")
    if not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")

    acquisition_log = pd.read_csv(log_path, dtype=str, keep_default_na=False)
    missing_columns = sorted(
        SOURCE_ACQUISITION_LOG_REQUIRED_COLUMNS.difference(acquisition_log.columns)
    )
    if missing_columns:
        return [f"Source acquisition log missing columns: {', '.join(missing_columns)}"]

    source_registry = pd.read_csv(source_registry_path, dtype=str, keep_default_na=False)
    source_by_id = {
        row["source_id"]: row for row in source_registry.to_dict("records") if row["source_id"]
    }

    errors: list[str] = []
    duplicate_ids = sorted(
        acquisition_log.loc[acquisition_log["source_id"].duplicated(), "source_id"]
        .dropna()
        .unique()
    )
    for source_id in duplicate_ids:
        errors.append(f"Duplicate source acquisition log row: {source_id}")

    status_counts = acquisition_log["status"].value_counts().to_dict()
    if status_counts.get("acquired", 0) < 8:
        errors.append("Source acquisition log must include at least 8 acquired sources")
    if status_counts.get("failed", 0) == 0:
        errors.append("Source acquisition log must preserve failed retrieval attempts")
    if status_counts.get("shell_html_not_evidence", 0) == 0:
        errors.append("Source acquisition log must preserve shell HTML rejections")

    logged_source_ids = set(acquisition_log["source_id"])
    for row in acquisition_log.to_dict("records"):
        source_id = row["source_id"].strip()
        if not source_id:
            errors.append("Source acquisition log contains a row with empty source_id")
            continue
        source_row = source_by_id.get(source_id)
        if source_row is None:
            errors.append(f"Source acquisition log references unknown source_id: {source_id}")
            continue

        status = row["status"].strip()
        if status not in SOURCE_ACQUISITION_STATUSES:
            errors.append(f"Source acquisition row {source_id} has invalid status: {status}")

        for column in ("attempted_url", "retrieval_date", "notes"):
            if not row[column].strip():
                errors.append(f"Source acquisition row {source_id} has empty {column}")

        retrieval_date = row["retrieval_date"].strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", retrieval_date):
            errors.append(
                f"Source acquisition row {source_id} has invalid retrieval_date: {retrieval_date}"
            )

        raw_path = row["raw_path"].strip()
        expected_hash = row["sha256"].strip()
        if status == "acquired":
            if not raw_path:
                errors.append(f"Acquired source acquisition row {source_id} has empty raw_path")
                continue
            if len(expected_hash) != 64 or any(
                char not in "0123456789abcdef" for char in expected_hash
            ):
                errors.append(f"Acquired source acquisition row {source_id} has invalid hash")
                continue
            candidate = Path(raw_path)
            if candidate.is_absolute() or ".." in candidate.parts:
                errors.append(f"Source acquisition row {source_id} has unsafe raw_path")
                continue
            raw_file = root / candidate
            if not raw_file.is_file():
                errors.append(f"Source acquisition raw file is missing: {raw_path}")
                continue
            actual_hash = hashlib.sha256(raw_file.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                errors.append(f"Source acquisition hash mismatch: {source_id}")
            if source_row["status"] != "acquired":
                errors.append(f"Acquired source {source_id} is not acquired in source registry")
            if source_row["raw_path"] != raw_path:
                errors.append(f"Source acquisition raw_path differs from registry: {source_id}")
            if source_row["sha256"] != expected_hash:
                errors.append(f"Source acquisition hash differs from registry: {source_id}")
        else:
            if raw_path or expected_hash:
                errors.append(f"Unacquired source acquisition row {source_id} must not carry hash")
            if source_row["status"] == "acquired":
                errors.append(
                    f"Unacquired source acquisition row {source_id} conflicts with registry"
                )

    for row in source_registry.to_dict("records"):
        raw_path = row["raw_path"].strip()
        if raw_path.startswith("data/raw/source_catalogues/"):
            source_id = row["source_id"]
            if source_id not in logged_source_ids:
                errors.append(f"Acquired source catalogue missing acquisition log: {source_id}")

    return errors


def validate_source_coverage_matrix(
    matrix_path: Path,
    source_registry_path: Path,
    gap_map_path: Path,
) -> list[str]:
    """Return validation errors for the historical source coverage matrix."""
    if not isinstance(matrix_path, Path):
        raise TypeError("matrix_path must be pathlib.Path")
    if not isinstance(source_registry_path, Path):
        raise TypeError("source_registry_path must be pathlib.Path")
    if not isinstance(gap_map_path, Path):
        raise TypeError("gap_map_path must be pathlib.Path")

    matrix = pd.read_csv(matrix_path, dtype=str, keep_default_na=False)
    missing_columns = sorted(SOURCE_COVERAGE_REQUIRED_COLUMNS.difference(matrix.columns))
    if missing_columns:
        return [f"Source coverage matrix missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    matrix["year_int"] = pd.to_numeric(matrix["year"], errors="coerce")
    invalid_year_rows = matrix[matrix["year_int"].isna()]
    for row_number in invalid_year_rows.index:
        errors.append(f"Source coverage row {row_number + 2} has invalid year")

    matrix = matrix[matrix["year_int"].notna()].copy()
    matrix["year_int"] = matrix["year_int"].astype(int)

    duplicate_rows = matrix[
        matrix.duplicated(subset=["variable_id", "year_int"], keep=False)
    ].sort_values(["variable_id", "year_int"])
    for row in duplicate_rows.to_dict("records"):
        errors.append(f"Duplicate source coverage row: {row['variable_id']} {row['year_int']}")

    observed_variables = set(matrix["variable_id"])
    for variable_id in sorted(SOURCE_COVERAGE_CORE_VARIABLES.difference(observed_variables)):
        errors.append(f"Missing source coverage variable: {variable_id}")

    required_pairs = {
        (variable_id, year)
        for variable_id in SOURCE_COVERAGE_CORE_VARIABLES
        for year in SOURCE_COVERAGE_YEARS
    }
    observed_pairs = set(zip(matrix["variable_id"], matrix["year_int"], strict=False))
    for variable_id, year in sorted(required_pairs.difference(observed_pairs)):
        errors.append(f"Missing source coverage row: {variable_id} {year}")

    extra_years = sorted(set(matrix["year_int"]).difference(SOURCE_COVERAGE_YEARS))
    for year in extra_years:
        errors.append(f"Source coverage matrix contains out-of-horizon year: {year}")

    extra_variables = sorted(observed_variables.difference(SOURCE_COVERAGE_CORE_VARIABLES))
    for variable_id in extra_variables:
        errors.append(f"Source coverage matrix contains unknown variable: {variable_id}")

    source_ids: set[str] = set()
    if source_registry_path.is_file():
        source_registry = pd.read_csv(source_registry_path, dtype=str, keep_default_na=False)
        if "source_id" in source_registry.columns:
            source_ids = set(source_registry["source_id"])

    for row in matrix.to_dict("records"):
        variable_id = row["variable_id"]
        year = row["year_int"]
        status = row["coverage_status"].strip()
        if status not in SOURCE_COVERAGE_STATUSES:
            errors.append(f"Source coverage row {variable_id} {year} has invalid status: {status}")

        for column in ("format", "granularity", "definition_break", "revision_status", "notes"):
            if not row[column].strip():
                errors.append(f"Source coverage row {variable_id} {year} has empty {column}")

        sources = _split_registry_values(row["source_id"])
        if status in {"observed", "definition-break", "revision-conflict"} and not sources:
            errors.append(f"Source coverage row {variable_id} {year} must include source_id")
        for source_id in sources:
            if source_id != "none" and source_ids and source_id not in source_ids:
                errors.append(
                    f"Source coverage row {variable_id} {year} references unknown source_id: "
                    f"{source_id}"
                )

    if not gap_map_path.is_file():
        errors.append(f"Missing historical data gap map: {gap_map_path}")
    else:
        text = gap_map_path.read_text(encoding="utf-8")
        for variable_id in sorted(SOURCE_COVERAGE_CORE_VARIABLES):
            if variable_id not in text:
                errors.append(f"Historical data gap map does not mention {variable_id}")
        if "Secondary estimates" not in text:
            errors.append("Historical data gap map must state the secondary-estimate rule")

    return errors


def validate_literature_map(
    map_path: Path,
    protocol_path: Path,
    synthesis_path: Path,
) -> list[str]:
    """Return validation errors for the literature and novelty map."""
    if not isinstance(map_path, Path):
        raise TypeError("map_path must be pathlib.Path")
    if not isinstance(protocol_path, Path):
        raise TypeError("protocol_path must be pathlib.Path")
    if not isinstance(synthesis_path, Path):
        raise TypeError("synthesis_path must be pathlib.Path")

    literature = pd.read_csv(map_path, dtype=str, keep_default_na=False)
    missing_columns = sorted(LITERATURE_MAP_REQUIRED_COLUMNS.difference(literature.columns))
    if missing_columns:
        return [f"Literature map missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicate_ids = sorted(
        literature.loc[literature["reference_id"].duplicated(), "reference_id"].dropna().unique()
    )
    for reference_id in duplicate_ids:
        errors.append(f"Duplicate literature reference_id: {reference_id}")

    included = literature[literature["inclusion_decision"].str.startswith("included_", na=False)]
    if len(included) < 8:
        errors.append("Literature map must include at least 8 included sources")

    nearest = included[included["novelty_role"] == "nearest_neighbor"]
    if len(nearest) < 4:
        errors.append("Literature map must identify at least 4 nearest-neighbor sources")

    academic_nearest = nearest[nearest["source_category"] == "academic_literature"]
    if len(academic_nearest) < 3:
        errors.append("Literature map must identify at least 3 academic nearest neighbors")

    for row in literature.to_dict("records"):
        reference_id = row["reference_id"].strip()
        if not reference_id:
            errors.append("Literature map contains a row with empty reference_id")
            continue

        for column in (
            "title",
            "authors",
            "venue",
            "topic",
            "research_question",
            "method",
            "data_period",
            "data_source",
            "main_finding",
            "relation_to_paper",
            "novelty_role",
            "search_database",
            "search_query",
            "search_date",
            "source_url",
        ):
            if not row[column].strip():
                errors.append(f"Literature row {reference_id} has empty {column}")

        category = row["source_category"].strip()
        if category not in LITERATURE_SOURCE_CATEGORIES:
            errors.append(f"Literature row {reference_id} has invalid source_category: {category}")

        decision = row["inclusion_decision"].strip()
        if decision not in LITERATURE_INCLUSION_DECISIONS:
            errors.append(
                f"Literature row {reference_id} has invalid inclusion_decision: {decision}"
            )

        search_date = row["search_date"].strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", search_date):
            errors.append(f"Literature row {reference_id} has invalid search_date: {search_date}")

        source_url = row["source_url"].strip()
        if not source_url.startswith(("https://", "http://")):
            errors.append(f"Literature row {reference_id} has invalid source_url: {source_url}")

        relation = row["relation_to_paper"].strip().lower()
        if "no paper" in relation or "not seen" in relation:
            errors.append(f"Literature row {reference_id} uses unsupported novelty language")

    for path, label in (
        (protocol_path, "literature search protocol"),
        (synthesis_path, "related-work synthesis"),
    ):
        if not path.is_file():
            errors.append(f"Missing {label}: {path}")
            continue
        text = path.read_text(encoding="utf-8").lower()
        if "evidence of absence" not in text:
            errors.append(f"{label} must include the bounded evidence-of-absence rule")
        if "proof" not in text:
            errors.append(f"{label} must explicitly reject proof-of-novelty language")

    return errors


def _split_registry_values(value: Any) -> list[str]:
    if pd.isna(value):
        return []
    text = str(value).strip()
    if not text or text.lower() in {"none", "not_applicable"}:
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def validate_concept_registry(registry_path: Path, root: Path) -> list[str]:
    """Return validation errors for the accounting ontology concept registry."""
    if not isinstance(registry_path, Path):
        raise TypeError("registry_path must be pathlib.Path")
    if not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")

    registry = pd.read_csv(registry_path, dtype=str, keep_default_na=False)
    missing_columns = sorted(CONCEPT_REGISTRY_REQUIRED_COLUMNS.difference(registry.columns))
    if missing_columns:
        return [f"Concept registry missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    concept_ids = set(registry["concept_id"])
    duplicate_ids = sorted(
        registry.loc[registry["concept_id"].duplicated(), "concept_id"].dropna().unique()
    )
    for concept_id in duplicate_ids:
        errors.append(f"Duplicate concept_id in concept registry: {concept_id}")

    for concept_id in sorted(REQUIRED_CONCEPT_IDS.difference(concept_ids)):
        errors.append(f"Missing required accounting concept: {concept_id}")

    source_ids: set[str] = set()
    source_registry_path = root / "evidence" / "source_registry.csv"
    if source_registry_path.is_file():
        source_registry = pd.read_csv(source_registry_path, dtype=str, keep_default_na=False)
        if "source_id" in source_registry.columns:
            source_ids = set(source_registry["source_id"])

    mapping_index: dict[tuple[str, str], str] = {}
    for row in registry.to_dict("records"):
        concept_id = row["concept_id"].strip()
        if not concept_id:
            errors.append("Concept registry contains a row with empty concept_id")
            continue

        for column in (
            "source_label",
            "canonical_name",
            "concept_class",
            "definition",
            "institutional_perimeter",
            "accounting_basis",
            "source_definition_status",
            "sign_convention",
        ):
            if not row[column].strip():
                errors.append(f"Concept {concept_id} has empty {column}")

        status = row["source_definition_status"].strip()
        if status and status not in CONCEPT_SOURCE_DEFINITION_STATUSES:
            errors.append(f"Concept {concept_id} has invalid source_definition_status: {status}")

        sign_convention = row["sign_convention"].strip()
        if sign_convention and sign_convention not in CONCEPT_SIGN_CONVENTIONS:
            errors.append(f"Concept {concept_id} has invalid sign_convention: {sign_convention}")

        if status == "source_defined" and not _split_registry_values(row["source_id"]):
            errors.append(f"Source-defined concept {concept_id} must include source_id")

        for source_id in _split_registry_values(row["source_id"]):
            if source_ids and source_id not in source_ids:
                errors.append(f"Concept {concept_id} references unknown source_id: {source_id}")

        guard = row["ambiguous_label_guard"].strip()
        searchable = " ".join(
            [
                row["source_label"],
                row["canonical_name"],
                row["definition"],
                row["internal_variable_names"],
            ]
        ).lower()
        if not guard:
            for term in AMBIGUOUS_ACCOUNTING_TERMS:
                if term in searchable:
                    errors.append(f"Concept {concept_id} must define ambiguous_label_guard")
                    break

        for mapping in _split_registry_values(row["material_flow_columns"]):
            if ":" not in mapping:
                errors.append(f"Concept {concept_id} has invalid material mapping: {mapping}")
                continue
            dataset, column = mapping.split(":", 1)
            dataset = dataset.strip().replace("\\", "/")
            column = column.strip()
            mapping_index[(dataset, column)] = concept_id
            dataset_path = root / Path(dataset)
            if not dataset_path.is_file():
                errors.append(f"Concept {concept_id} maps missing dataset: {dataset}")
                continue
            dataset_columns = pd.read_csv(dataset_path, nrows=0).columns
            if column not in dataset_columns:
                errors.append(f"Concept {concept_id} maps missing column: {dataset}:{column}")

    for dataset, column in sorted(REQUIRED_MATERIAL_FLOW_MAPPINGS):
        concept_id = mapping_index.get((dataset, column))
        if concept_id is None:
            errors.append(f"Missing concept mapping for material column: {dataset}:{column}")
        elif concept_id not in concept_ids:
            errors.append(
                f"Material column {dataset}:{column} maps to unknown concept: {concept_id}"
            )

    return errors


def validate_analysis_protocol(protocol_path: Path, hash_path: Path) -> list[str]:
    """Return validation errors for the preregistered analysis protocol."""
    if not isinstance(protocol_path, Path):
        raise TypeError("protocol_path must be pathlib.Path")
    if not isinstance(hash_path, Path):
        raise TypeError("hash_path must be pathlib.Path")

    protocol = pd.read_csv(protocol_path, dtype=str)
    required_columns = {
        "hypothesis_id",
        "estimand_id",
        "formula",
        "numerator",
        "denominator",
        "population",
        "period",
        "unit",
        "accounting_basis",
        "perimeter",
        "primary_sources",
        "tolerance_rule",
        "materiality_rule",
        "falsification_rule",
        "exploratory_or_confirmatory",
        "counterfactual_class",
        "alternative_perimeter_set",
        "required_source_class",
        "protocol_version",
        "status",
    }
    missing_columns = sorted(required_columns.difference(protocol.columns))
    if missing_columns:
        return [f"Analysis protocol missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    observed_hypotheses = set(protocol["hypothesis_id"].dropna().astype(str))
    for hypothesis_id in sorted(
        REQUIRED_ANALYSIS_PROTOCOL_HYPOTHESES.difference(observed_hypotheses)
    ):
        errors.append(f"Missing analysis protocol hypothesis: {hypothesis_id}")

    duplicates = protocol[protocol.duplicated(subset=["hypothesis_id", "estimand_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            "Duplicate analysis protocol estimand: "
            f"{_registry_field(duplicate_row, 'hypothesis_id')} "
            f"{_registry_field(duplicate_row, 'estimand_id')}"
        )

    allowed_statuses = {"defined_requires_sources", "partial_bounded_reconstruction"}
    allowed_modes = {"confirmatory", "exploratory"}
    allowed_counterfactual_classes = {
        "economic_scenario",
        "legal_replication",
        "not_applicable",
    }
    protocol_versions = set(protocol["protocol_version"].dropna().astype(str))
    if protocol_versions != {"0.3.0"}:
        errors.append("Analysis protocol must use exactly protocol_version 0.3.0")

    for row_number, record in enumerate(protocol.to_dict("records"), start=2):
        hypothesis_id = _registry_field(record, "hypothesis_id") or f"row {row_number}"
        for column in required_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on analysis protocol row {row_number}")

        status = _registry_field(record, "status")
        if status and status not in allowed_statuses:
            errors.append(f"Unexpected analysis protocol status on row {row_number}: {status}")

        mode = _registry_field(record, "exploratory_or_confirmatory")
        if mode and mode not in allowed_modes:
            errors.append(f"Unexpected analysis protocol mode on row {row_number}: {mode}")

        counterfactual_class = _registry_field(record, "counterfactual_class")
        if counterfactual_class and counterfactual_class not in allowed_counterfactual_classes:
            errors.append(
                f"Unexpected counterfactual_class on analysis protocol row {row_number}: "
                f"{counterfactual_class}"
            )

        if status == "defined_requires_sources" and _registry_field(
            record, "required_source_class"
        ) in {"", "not_applicable"}:
            errors.append(f"Analysis protocol row {hypothesis_id} must name required sources")

        if "material" not in _registry_field(record, "materiality_rule").lower():
            errors.append(f"Analysis protocol row {hypothesis_id} must define materiality")

    if not hash_path.is_file():
        errors.append("Missing analysis protocol hash file: analysis_protocol_hash.csv")
        return errors

    hash_registry = pd.read_csv(hash_path, dtype=str)
    hash_columns = {"protocol_version", "artifact_path", "sha256", "status", "notes"}
    missing_hash_columns = sorted(hash_columns.difference(hash_registry.columns))
    if missing_hash_columns:
        errors.append(f"Analysis protocol hash missing columns: {', '.join(missing_hash_columns)}")
        return errors
    if len(hash_registry) != 1:
        errors.append("Analysis protocol hash must contain exactly one row")
        return errors

    row = hash_registry.iloc[0]
    expected_hash = _registry_field(row, "sha256").lower()
    actual_hash = hashlib.sha256(manifest_bytes(protocol_path)).hexdigest()
    if expected_hash != actual_hash:
        errors.append("Analysis protocol hash does not match analysis_protocol.csv")
    if _registry_field(row, "protocol_version") != "0.3.0":
        errors.append("Analysis protocol hash must use protocol_version 0.3.0")
    if _registry_field(row, "artifact_path") != "evidence/analysis_protocol.csv":
        errors.append("Analysis protocol hash artifact_path is incorrect")

    return errors


def validate_falsification_review(path: Path) -> list[str]:
    """Return validation errors for the adversarial falsification review ledger."""
    if not isinstance(path, Path):
        raise TypeError("path must be pathlib.Path")
    review = pd.read_csv(path, dtype=str)
    required_columns = {
        "test_id",
        "challenge",
        "target_module",
        "adversarial_hypothesis",
        "evidence_required",
        "current_evidence",
        "result_class",
        "decision",
        "unit",
        "source_ids",
        "blocking_issue",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(review.columns))
    if missing_columns:
        return [f"Falsification review missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicated_ids = review[review.duplicated(subset=["test_id"], keep=False)]
    for _, duplicate_row in duplicated_ids.iterrows():
        errors.append(
            f"Duplicate falsification review row: {_registry_field(duplicate_row, 'test_id')}"
        )

    observed_tests = set(review["test_id"].dropna().astype(str))
    for test_id in sorted(REQUIRED_FALSIFICATION_TESTS.difference(observed_tests)):
        errors.append(f"Missing required falsification test: {test_id}")
    for test_id in sorted(observed_tests.difference(REQUIRED_FALSIFICATION_TESTS)):
        errors.append(f"Unexpected falsification test: {test_id}")

    allowed_result_classes = {
        "not_testable_yet",
        "bounded_no_overturn",
        "partially_reconciled",
        "overturned",
    }
    allowed_decisions = {
        "unresolved_requires_sources",
        "unresolved_quantification",
        "not_overturned_bounded",
        "overturned",
    }
    allowed_statuses = {
        "blocked_missing_inputs",
        "partial_bounded_review",
        "complete",
    }
    for row_number, record in enumerate(review.to_dict("records"), start=2):
        for column in required_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on falsification review row {row_number}")

        result_class = _registry_field(record, "result_class")
        if result_class and result_class not in allowed_result_classes:
            errors.append(
                f"Unexpected result_class on falsification review row {row_number}: {result_class}"
            )

        decision = _registry_field(record, "decision")
        if decision and decision not in allowed_decisions:
            errors.append(
                f"Unexpected decision on falsification review row {row_number}: {decision}"
            )

        status = _registry_field(record, "status")
        if status and status not in allowed_statuses:
            errors.append(f"Unexpected status on falsification review row {row_number}: {status}")

        if decision.startswith("unresolved") and not _registry_field(record, "blocking_issue"):
            errors.append(f"Unresolved falsification row {row_number} must name blocking_issue")
        if status == "complete" and result_class == "not_testable_yet":
            errors.append(f"Complete falsification row {row_number} cannot be not_testable_yet")
        if _registry_field(record, "unit") != "EUR_million":
            errors.append(f"Falsification review row {row_number} must use EUR_million unit")
    return errors


def validate_publication_artifacts(
    figure_registry_path: Path,
    table_registry_path: Path,
    root: Path,
) -> list[str]:
    """Return validation errors for publication figure and table companion CSVs."""
    if not isinstance(figure_registry_path, Path):
        raise TypeError("figure_registry_path must be pathlib.Path")
    if not isinstance(table_registry_path, Path):
        raise TypeError("table_registry_path must be pathlib.Path")
    if not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")

    figure_registry = pd.read_csv(figure_registry_path, dtype=str)
    table_registry = pd.read_csv(table_registry_path, dtype=str)
    errors = [
        *_validate_publication_registry(
            figure_registry,
            root,
            id_column="figure_id",
            required_ids=REQUIRED_PUBLICATION_FIGURES,
            registry_name="figure registry",
            companion_column="companion_csv",
            allowed_statuses={"ready", "ready_partial", "blocked"},
            source_must_be_processed=True,
        ),
        *_validate_publication_registry(
            table_registry,
            root,
            id_column="table_id",
            required_ids=None,
            registry_name="table registry",
            companion_column="companion_csv",
            allowed_statuses={"ready", "ready_partial", "blocked"},
            source_must_be_processed=False,
        ),
    ]
    return errors


def validate_article_evidence(
    article_evidence_path: Path,
    claim_registry_path: Path,
    figure_registry_path: Path,
    table_registry_path: Path,
    root: Path,
) -> list[str]:
    """Return validation errors for article evidence provenance gates."""
    for name, path in (
        ("article_evidence_path", article_evidence_path),
        ("claim_registry_path", claim_registry_path),
        ("figure_registry_path", figure_registry_path),
        ("table_registry_path", table_registry_path),
        ("root", root),
    ):
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")

    evidence = pd.read_csv(article_evidence_path, dtype=str)
    claims = pd.read_csv(claim_registry_path, dtype=str)
    figure_registry = pd.read_csv(figure_registry_path, dtype=str)
    table_registry = pd.read_csv(table_registry_path, dtype=str)

    required_columns = {
        "evidence_id",
        "claim_id",
        "manuscript_section",
        "claim_status",
        "source_ids",
        "raw_value",
        "transformation",
        "processed_dataset",
        "output_artifact",
        "unit",
        "provenance_status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(evidence.columns))
    if missing_columns:
        return [f"Article evidence missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = evidence[evidence.duplicated(subset=["evidence_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate article evidence row: {_registry_field(duplicate_row, 'evidence_id')}"
        )

    claim_records = {
        _registry_field(record, "claim_id"): record for record in claims.to_dict("records")
    }
    material_claim_ids = {
        _registry_field(record, "claim_id")
        for record in claims.to_dict("records")
        if _registry_field(record, "claim_type") in ARTICLE_EVIDENCE_REQUIRED_CLAIM_TYPES
        and _registry_field(record, "status") not in {"source_registered", "source_acquired"}
    }
    evidence_claim_ids = set(evidence["claim_id"].dropna().astype(str))
    for claim_id in sorted(material_claim_ids.difference(evidence_claim_ids)):
        errors.append(f"Material claim missing article evidence: {claim_id}")

    figure_outputs = set(figure_registry["companion_csv"].dropna().astype(str))
    table_outputs = set(table_registry["companion_csv"].dropna().astype(str))
    allowed_outputs = figure_outputs.union(table_outputs).union({"evidence/article_evidence.md"})
    allowed_provenance_statuses = {"ready_for_bounded_article_use", "bounded_only"}

    for row_number, record in enumerate(evidence.to_dict("records"), start=2):
        evidence_id = _registry_field(record, "evidence_id") or f"row {row_number}"
        for column in required_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on article evidence row {row_number}")

        claim_id = _registry_field(record, "claim_id")
        claim = claim_records.get(claim_id)
        if claim is None:
            errors.append(f"Article evidence {evidence_id} references unknown claim: {claim_id}")
        else:
            claim_status = _registry_field(claim, "status")
            if claim_status in ARTICLE_EVIDENCE_BLOCKING_STATUSES:
                errors.append(
                    f"Article evidence {evidence_id} uses blocking claim status: {claim_status}"
                )
            if claim_status != _registry_field(record, "claim_status"):
                errors.append(
                    f"Article evidence {evidence_id} claim_status does not match registry"
                )
            if not _registry_field(claim, "falsification_condition"):
                errors.append(f"Article evidence {evidence_id} claim lacks falsification condition")

        processed_dataset = _registry_field(record, "processed_dataset")
        if processed_dataset:
            if Path(processed_dataset).is_absolute() or ".." in Path(processed_dataset).parts:
                errors.append(f"Article evidence {evidence_id} has unsafe processed_dataset")
            elif not (root / processed_dataset).is_file():
                errors.append(
                    f"Article evidence {evidence_id} processed_dataset is missing: "
                    f"{processed_dataset}"
                )

        output_artifact = _registry_field(record, "output_artifact")
        if output_artifact and output_artifact not in allowed_outputs:
            errors.append(f"Article evidence {evidence_id} output_artifact is not registered")
        if output_artifact and not (root / output_artifact).is_file():
            errors.append(f"Article evidence {evidence_id} output_artifact is missing")

        provenance_status = _registry_field(record, "provenance_status")
        if provenance_status and provenance_status not in allowed_provenance_statuses:
            errors.append(
                f"Unexpected provenance_status on article evidence row {row_number}: "
                f"{provenance_status}"
            )

    errors.extend(
        _validate_evidence_level_artifact_registry(
            figure_registry,
            root,
            registry_name="evidence figure registry",
            id_column="figure_id",
            required_ids=REQUIRED_PUBLICATION_FIGURES,
        )
    )
    errors.extend(
        _validate_evidence_level_artifact_registry(
            table_registry,
            root,
            registry_name="evidence table registry",
            id_column="table_id",
            required_ids=None,
        )
    )
    return errors


def validate_manuscript_draft(
    manuscript_path: Path,
    article_evidence_path: Path,
) -> list[str]:
    """Return validation errors for the bounded manuscript draft."""
    if not isinstance(manuscript_path, Path):
        raise TypeError("manuscript_path must be pathlib.Path")
    if not isinstance(article_evidence_path, Path):
        raise TypeError("article_evidence_path must be pathlib.Path")

    text = manuscript_path.read_text(encoding="utf-8")
    article_evidence = pd.read_csv(article_evidence_path, dtype=str)
    errors: list[str] = []

    required_labels = {
        "[Legal fact]",
        "[Accounting fact]",
        "[Interpretation]",
        "[Unresolved evidence]",
        "[Counterfactual result]",
        "[Actuarial assumption]",
    }
    for label in sorted(required_labels):
        if label not in text:
            errors.append(f"Manuscript missing required label: {label}")

    for evidence_id in article_evidence["evidence_id"].dropna().astype(str):
        if evidence_id not in text:
            errors.append(f"Manuscript does not reference article evidence row: {evidence_id}")

    required_gate_phrases = {
        "does not yet support definitive claims",
        "does not establish",
        "does not classify",
        "No numerical counterfactual result is reported",
        "Reproducing the published combined-balance definition would not endorse it",
    }
    for phrase in sorted(required_gate_phrases):
        if phrase not in text:
            errors.append(f"Manuscript missing evidence-boundary phrase: {phrase}")

    unsupported_phrases = {
        "proves that CGA",
        "proves Social Security",
        "definitive remittance loss",
        "definitive employer underpayment",
        "bank-transfer subsidy",
        "lifecycle public-finance loss.",
    }
    lowered_text = text.lower()
    for phrase in sorted(unsupported_phrases):
        if phrase.lower() in lowered_text:
            errors.append(f"Manuscript contains unsupported phrase: {phrase}")

    return errors


def validate_combined_balance_replication(
    replication_path: Path,
    bridge_path: Path,
) -> list[str]:
    """Return validation errors for the 2026 combined-balance replication gate."""
    for name, path in (("replication_path", replication_path), ("bridge_path", bridge_path)):
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")

    replication = pd.read_csv(replication_path, dtype=str, keep_default_na=False)
    bridge = pd.read_csv(bridge_path, dtype=str, keep_default_na=False)
    required_replication_columns = {
        "series_id",
        "year",
        "definition_id",
        "definition_role",
        "component",
        "value",
        "unit",
        "source_ids",
        "component_bridge_ids",
        "sign_effect_class",
        "replication_status",
        "blocking_issue",
        "notes",
    }
    required_bridge_columns = {
        "bridge_id",
        "definition_id",
        "component",
        "component_role",
        "operation",
        "source_requirement",
        "sign_effect_class",
        "bank_special_regime_visibility",
        "replication_status",
        "blocking_issue",
        "notes",
    }
    errors: list[str] = []
    missing_replication_columns = sorted(
        required_replication_columns.difference(replication.columns)
    )
    if missing_replication_columns:
        return [
            "Combined balance replication table missing columns: "
            f"{', '.join(missing_replication_columns)}"
        ]
    missing_bridge_columns = sorted(required_bridge_columns.difference(bridge.columns))
    if missing_bridge_columns:
        return [
            "Combined balance component bridge missing columns: "
            f"{', '.join(missing_bridge_columns)}"
        ]

    required_definitions = {
        "alternative_cga_only",
        "alternative_cga_plus_previdential_plus_fefss",
        "alternative_cga_plus_previdential_unadjusted",
        "bank_special_regime_sensitivity",
        "published_working_group_adjusted_2025",
        "published_working_group_definition",
    }
    observed_definitions = set(replication["definition_id"])
    for definition_id in sorted(required_definitions.difference(observed_definitions)):
        errors.append(f"Missing combined-balance definition: {definition_id}")

    published_years = {
        int(year)
        for year in replication.loc[
            (replication["definition_id"] == "published_working_group_definition")
            & (replication["component"] == "reported_combined_total"),
            "year",
        ]
        if year.isdigit()
    }
    for year in range(2006, 2026):
        if year not in published_years:
            errors.append(f"Missing published combined-balance annual row: {year}")

    required_bridge_ids = {
        "BR_BANK_SPECIAL_SENSITIVITY",
        "BR_CGA_BALANCE",
        "BR_EARLY_RETIREMENT_ADJUSTMENT",
        "BR_FEFSS_FLOW_ALTERNATIVE",
        "BR_OTHER_RECLASSIFICATIONS",
        "BR_PREVIDENTIAL_BALANCE",
    }
    observed_bridge_ids = set(bridge["bridge_id"])
    for bridge_id in sorted(required_bridge_ids.difference(observed_bridge_ids)):
        errors.append(f"Missing combined-balance component bridge row: {bridge_id}")

    allowed_roles = {"alternative_perimeter", "published_definition", "sensitivity"}
    allowed_statuses = {
        "approximately_reproduced",
        "blocked_primary_source_missing",
        "not_reproduced",
        "reproduced",
    }
    allowed_sign_effects = {"magnitude_only", "not_applicable", "sensitivity_only", "sign_relevant"}
    bridge_ids = set(bridge["bridge_id"])
    for row_number, record in enumerate(replication.to_dict("records"), start=2):
        for column in required_replication_columns.difference({"value"}):
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on combined-balance row {row_number}")
        if _registry_field(record, "definition_role") not in allowed_roles:
            errors.append(f"Unexpected combined-balance definition_role on row {row_number}")
        status = _registry_field(record, "replication_status")
        if status not in allowed_statuses:
            errors.append(f"Unexpected combined-balance replication_status on row {row_number}")
        sign_effect = _registry_field(record, "sign_effect_class")
        if sign_effect not in allowed_sign_effects:
            errors.append(f"Unexpected combined-balance sign_effect_class on row {row_number}")
        if status == "blocked_primary_source_missing":
            if _registry_field(record, "value"):
                errors.append(
                    f"Blocked combined-balance row must not contain value on row {row_number}"
                )
            if "primary" not in _registry_field(record, "blocking_issue").lower():
                errors.append(
                    "Blocked combined-balance row must name the missing primary "
                    f"source on row {row_number}"
                )
        for bridge_id in _registry_field(record, "component_bridge_ids").split(";"):
            if bridge_id and bridge_id not in bridge_ids:
                errors.append(
                    f"Combined-balance row {row_number} references unknown bridge: {bridge_id}"
                )

    for row_number, record in enumerate(bridge.to_dict("records"), start=2):
        for column in required_bridge_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on combined-balance bridge row {row_number}")
        status = _registry_field(record, "replication_status")
        if status not in allowed_statuses:
            errors.append(
                f"Unexpected combined-balance bridge replication_status on row {row_number}"
            )
        sign_effect = _registry_field(record, "sign_effect_class")
        if sign_effect not in allowed_sign_effects:
            errors.append(
                f"Unexpected combined-balance bridge sign_effect_class on row {row_number}"
            )
        if status == "blocked_primary_source_missing" and (
            "primary" not in _registry_field(record, "blocking_issue").lower()
        ):
            errors.append(
                "Blocked combined-balance bridge row must name the missing primary "
                f"source on row {row_number}"
            )
    return errors


def validate_joint_balance_definitions(
    definitions_path: Path,
    rules_path: Path,
) -> list[str]:
    """Return validation errors for competing CGA/RGSS balance definitions."""
    for name, path in (("definitions_path", definitions_path), ("rules_path", rules_path)):
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")

    definitions = pd.read_csv(definitions_path, dtype=str, keep_default_na=False)
    rules = pd.read_csv(rules_path, dtype=str, keep_default_na=False)
    required_definition_columns = {
        "definition_id",
        "definition_label",
        "definition_role",
        "period",
        "unit",
        "accounting_basis",
        "perimeter",
        "inclusion_rule_ids",
        "exclusion_rule_ids",
        "consolidation_rule",
        "bank_special_regime_treatment",
        "historical_adjustment_policy",
        "source_requirements",
        "status",
        "blocking_issue",
        "notes",
    }
    required_rule_columns = {
        "rule_id",
        "rule_type",
        "component",
        "operation",
        "sign_convention",
        "double_counting_guard",
        "unit_requirement",
        "source_requirement",
        "status",
        "blocking_issue",
        "notes",
    }
    errors: list[str] = []
    missing_definition_columns = sorted(required_definition_columns.difference(definitions.columns))
    if missing_definition_columns:
        return [
            f"Joint balance definitions missing columns: {', '.join(missing_definition_columns)}"
        ]
    missing_rule_columns = sorted(required_rule_columns.difference(rules.columns))
    if missing_rule_columns:
        return [
            f"Joint balance definition rules missing columns: {', '.join(missing_rule_columns)}"
        ]

    required_definitions = {
        "BANK_SPECIAL_SEPARATE_SENSITIVITY",
        "CGA_INSTITUTIONAL_BALANCE",
        "CONSOLIDATED_GENERAL_GOVERNMENT",
        "FEFSS_VISIBLE_ALTERNATIVE",
        "HISTORICALLY_ADJUSTED_NO_EARLY_RETIREMENT",
        "HISTORICALLY_ADJUSTED_WORKING_GROUP",
        "RGSS_PREVIDENTIAL_REPORTED",
        "SIMPLE_CGA_PREVIDENTIAL_COMBINED",
    }
    observed_definitions = set(definitions["definition_id"])
    for definition_id in sorted(required_definitions.difference(observed_definitions)):
        errors.append(f"Missing joint balance definition: {definition_id}")

    required_rules = {
        "EXC_BANK_SPECIAL_OBLIGATIONS",
        "EXC_CGA_BALANCE",
        "EXC_EARLY_RETIREMENT_ADJUSTMENT",
        "EXC_FEFSS_STOCK",
        "EXC_INTRA_PUBLIC_TRANSFERS",
        "EXC_PREVIDENTIAL_BALANCE",
        "INC_BANK_SPECIAL_OBLIGATIONS",
        "INC_CGA_BALANCE",
        "INC_CONSOLIDATION_ELIMINATIONS",
        "INC_FEFSS_FLOW",
        "INC_HISTORICAL_ADJUSTMENTS",
        "INC_PREVIDENTIAL_BALANCE",
    }
    observed_rules = set(rules["rule_id"])
    for rule_id in sorted(required_rules.difference(observed_rules)):
        errors.append(f"Missing joint balance rule: {rule_id}")

    allowed_definition_roles = {
        "alternative_perimeter",
        "base_perimeter",
        "combined_perimeter",
        "consolidated_perimeter",
        "historical_adjustment_variant",
        "sensitivity_perimeter",
    }
    allowed_rule_types = {"exclusion", "inclusion"}
    allowed_statuses = {
        "blocked_primary_source_missing",
        "ready_for_calculation",
    }
    duplicates = definitions[definitions.duplicated(subset=["definition_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate joint balance definition: {_registry_field(duplicate_row, 'definition_id')}"
        )
    duplicate_rules = rules[rules.duplicated(subset=["rule_id"], keep=False)]
    for _, duplicate_row in duplicate_rules.iterrows():
        errors.append(f"Duplicate joint balance rule: {_registry_field(duplicate_row, 'rule_id')}")

    for row_number, record in enumerate(definitions.to_dict("records"), start=2):
        for column in required_definition_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on joint balance definition row {row_number}")
        if _registry_field(record, "definition_role") not in allowed_definition_roles:
            errors.append(f"Unexpected joint balance definition_role on row {row_number}")
        if _registry_field(record, "unit") != "EUR_million":
            errors.append(f"Unexpected joint balance unit on row {row_number}")
        if _registry_field(record, "status") not in allowed_statuses:
            errors.append(f"Unexpected joint balance status on row {row_number}")
        if _registry_field(record, "status") == "blocked_primary_source_missing" and (
            "primary" not in _registry_field(record, "blocking_issue").lower()
        ):
            errors.append(
                "Blocked joint balance definition must name the missing primary "
                f"source on row {row_number}"
            )
        referenced_rules = set(
            filter(
                None,
                (
                    _registry_field(record, "inclusion_rule_ids")
                    + ";"
                    + _registry_field(record, "exclusion_rule_ids")
                ).split(";"),
            )
        )
        for rule_id in sorted(referenced_rules.difference(observed_rules)):
            errors.append(
                f"Joint balance definition row {row_number} references unknown rule: {rule_id}"
            )
        if _registry_field(record, "definition_id") == "CONSOLIDATED_GENERAL_GOVERNMENT" and (
            "eliminate" not in _registry_field(record, "consolidation_rule")
        ):
            errors.append("Consolidated general-government definition must eliminate transfers")
        if _registry_field(record, "definition_id") == "BANK_SPECIAL_SEPARATE_SENSITIVITY" and (
            "sensitivity" not in _registry_field(record, "bank_special_regime_treatment")
        ):
            errors.append("Bank special-regime definition must remain a visible sensitivity")

    for row_number, record in enumerate(rules.to_dict("records"), start=2):
        for column in required_rule_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on joint balance rule row {row_number}")
        if _registry_field(record, "rule_type") not in allowed_rule_types:
            errors.append(f"Unexpected joint balance rule_type on row {row_number}")
        if _registry_field(record, "unit_requirement") != "EUR_million":
            errors.append(f"Unexpected joint balance unit_requirement on row {row_number}")
        if _registry_field(record, "status") not in allowed_statuses:
            errors.append(f"Unexpected joint balance rule status on row {row_number}")
        if not _registry_field(record, "double_counting_guard"):
            errors.append(f"Missing double-counting guard on joint balance rule row {row_number}")
        if _registry_field(record, "status") == "blocked_primary_source_missing" and (
            "primary" not in _registry_field(record, "blocking_issue").lower()
        ):
            errors.append(
                "Blocked joint balance rule must name the missing primary "
                f"source on row {row_number}"
            )
    return errors


def validate_public_claim_registry(
    public_claim_path: Path,
    replication_path: Path,
) -> list[str]:
    """Return validation errors for public claim replication targets."""
    for name, path in (
        ("public_claim_path", public_claim_path),
        ("replication_path", replication_path),
    ):
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")

    claims = pd.read_csv(public_claim_path, dtype=str, keep_default_na=False)
    replication = pd.read_csv(replication_path, dtype=str, keep_default_na=False)
    required_claim_columns = {
        "claim_id",
        "claim_target",
        "claimant_or_report",
        "report_component",
        "claim_text",
        "quantity",
        "unit",
        "period",
        "perimeter",
        "primary_source_ids",
        "identification_source_ids",
        "processed_dataset",
        "replication_status",
        "replicated_value",
        "method_status",
        "blocking_issue",
        "notes",
    }
    required_replication_columns = {
        "claim_id",
        "claim_target",
        "input_artifacts",
        "transformation",
        "replication_status",
        "replicated_value",
        "residual",
        "unit",
        "blocking_issue",
        "notes",
    }
    errors: list[str] = []
    missing_claim_columns = sorted(required_claim_columns.difference(claims.columns))
    if missing_claim_columns:
        return [f"Public claim registry missing columns: {', '.join(missing_claim_columns)}"]
    missing_replication_columns = sorted(
        required_replication_columns.difference(replication.columns)
    )
    if missing_replication_columns:
        return [
            "Working group replication table missing columns: "
            f"{', '.join(missing_replication_columns)}"
        ]

    required_targets = {
        "post_2006_public_worker_contributions",
        "fefss_capitalization",
        "share_of_fefss",
        "combined_cga_previdential_balance",
        "adjusted_2025_deficit",
    }
    observed_targets = set(claims["claim_target"])
    for target in sorted(required_targets.difference(observed_targets)):
        errors.append(f"Missing public claim target: {target}")

    allowed_statuses = {
        "reproduced",
        "approximately_reproduced",
        "not_reproduced",
        "not_identifiable",
        "blocked_primary_source_missing",
    }
    duplicates = claims[claims.duplicated(subset=["claim_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(f"Duplicate public claim_id: {_registry_field(duplicate_row, 'claim_id')}")

    replication_ids = set(replication["claim_id"])
    for row_number, record in enumerate(claims.to_dict("records"), start=2):
        claim_id = _registry_field(record, "claim_id")
        if claim_id not in replication_ids:
            errors.append(f"Public claim missing replication companion row: {claim_id}")
        for column in required_claim_columns.difference(
            {
                "quantity",
                "primary_source_ids",
                "identification_source_ids",
                "replicated_value",
            }
        ):
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on public claim row {row_number}")
        status = _registry_field(record, "replication_status")
        if status not in allowed_statuses:
            errors.append(
                f"Unexpected public claim replication_status on row {row_number}: {status}"
            )
        if status in {"not_identifiable", "blocked_primary_source_missing"}:
            if _registry_field(record, "quantity") or _registry_field(record, "replicated_value"):
                errors.append(
                    "Blocked public claim rows must not contain copied or replicated values "
                    f"on row {row_number}"
                )
            if "primary" not in _registry_field(record, "blocking_issue").lower():
                errors.append(
                    "Blocked public claim row must name the missing primary "
                    f"source on row {row_number}"
                )
        if _registry_field(record, "processed_dataset"):
            processed_dataset = Path(_registry_field(record, "processed_dataset"))
            if processed_dataset.is_absolute() or ".." in processed_dataset.parts:
                errors.append(f"Unsafe processed_dataset on public claim row {row_number}")

    claim_ids = set(claims["claim_id"])
    for row_number, record in enumerate(replication.to_dict("records"), start=2):
        claim_id = _registry_field(record, "claim_id")
        if claim_id not in claim_ids:
            errors.append(f"Replication companion references unknown public claim: {claim_id}")
        status = _registry_field(record, "replication_status")
        if status not in allowed_statuses:
            errors.append(
                f"Unexpected working group replication_status on row {row_number}: {status}"
            )
        if status in {"not_identifiable", "blocked_primary_source_missing"}:
            if _registry_field(record, "replicated_value") or _registry_field(record, "residual"):
                errors.append(
                    "Blocked working group replication rows must not contain values "
                    f"on row {row_number}"
                )
            if "primary" not in _registry_field(record, "blocking_issue").lower():
                errors.append(
                    "Blocked working group replication row must name the missing primary "
                    f"source on row {row_number}"
                )
    return errors


def validate_internal_replication_review(
    review_path: Path,
    article_evidence_path: Path,
) -> list[str]:
    """Return validation errors for the internal replication review ledger."""
    if not isinstance(review_path, Path):
        raise TypeError("review_path must be pathlib.Path")
    if not isinstance(article_evidence_path, Path):
        raise TypeError("article_evidence_path must be pathlib.Path")

    review = pd.read_csv(review_path, dtype=str)
    article_evidence = pd.read_csv(article_evidence_path, dtype=str)

    required_columns = {
        "review_id",
        "target_area",
        "target_claim_ids",
        "input_artifacts",
        "source_ids",
        "period",
        "unit",
        "perimeter",
        "accounting_basis",
        "check_type",
        "independent_result",
        "residual",
        "alternative_definition_effect",
        "decision",
        "status",
        "blocking_issue",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(review.columns))
    if missing_columns:
        return [f"Internal replication review missing columns: {', '.join(missing_columns)}"]

    required_review_ids = {
        "REPL_ACCOUNTING_IDENTITIES",
        "REPL_BANK_PERIMETER",
        "REPL_CLAIM_REGISTRY",
        "REPL_COUNTERFACTUAL_BUDGET",
        "REPL_DISCOUNT_RATE",
        "REPL_ESA_TREATMENT",
        "REPL_LEGAL_CHRONOLOGY",
        "REPL_MANUSCRIPT_LANGUAGE",
        "REPL_MISSING_VALUES",
        "REPL_STATE_FINANCING",
    }
    observed_review_ids = set(review["review_id"].dropna().astype(str))
    errors: list[str] = []
    for review_id in sorted(required_review_ids.difference(observed_review_ids)):
        errors.append(f"Missing internal replication review row: {review_id}")

    duplicates = review[review.duplicated(subset=["review_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate internal replication review row: "
            f"{_registry_field(duplicate_row, 'review_id')}"
        )

    allowed_decisions = {
        "classification_confirmed",
        "no_overstatement_detected",
        "replicated_bounded",
        "unresolved_requires_sources",
    }
    allowed_statuses = {
        "blocked_missing_inputs",
        "complete",
        "partial_bounded_review",
    }
    covered_claim_ids: set[str] = set()
    for row_number, record in enumerate(review.to_dict("records"), start=2):
        review_id = _registry_field(record, "review_id") or f"row {row_number}"
        for column in required_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on internal replication review row {row_number}")

        decision = _registry_field(record, "decision")
        if decision and decision not in allowed_decisions:
            errors.append(
                f"Unexpected decision on internal replication review row {row_number}: {decision}"
            )

        status = _registry_field(record, "status")
        if status and status not in allowed_statuses:
            errors.append(
                f"Unexpected status on internal replication review row {row_number}: {status}"
            )

        blocking_issue = _registry_field(record, "blocking_issue")
        if status == "blocked_missing_inputs" and blocking_issue in {"", "none"}:
            errors.append(f"Blocked internal replication row {review_id} must name a blocker")
        if decision == "unresolved_requires_sources" and status != "blocked_missing_inputs":
            errors.append(f"Unresolved internal replication row {review_id} must be blocked")

        residual = _registry_field(record, "residual")
        if residual not in {"not_applicable", ""}:
            try:
                float(residual)
            except ValueError:
                errors.append(f"Internal replication row {review_id} has nonnumeric residual")

        for artifact in _registry_field(record, "input_artifacts").split(";"):
            artifact_path = Path(artifact)
            if artifact_path.is_absolute() or ".." in artifact_path.parts:
                errors.append(f"Unsafe input artifact on internal replication row {review_id}")

        covered_claim_ids.update(
            claim_id
            for claim_id in _registry_field(record, "target_claim_ids").split(";")
            if claim_id
            and not claim_id.startswith("evidence_")
            and claim_id != "article_evidence_gate"
        )

    article_claim_ids = set(article_evidence["claim_id"].dropna().astype(str))
    for claim_id in sorted(article_claim_ids.difference(covered_claim_ids)):
        errors.append(f"Article evidence claim missing replication review: {claim_id}")

    return errors


def validate_release_reproducibility_audit(
    audit_path: Path,
    root: Path,
) -> list[str]:
    """Return validation errors for the release-readiness audit ledger."""
    if not isinstance(audit_path, Path):
        raise TypeError("audit_path must be pathlib.Path")
    if not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")

    audit = pd.read_csv(audit_path, dtype=str)
    required_columns = {
        "check_id",
        "release_area",
        "input_artifacts",
        "command_or_gate",
        "period",
        "unit",
        "perimeter",
        "accounting_basis",
        "result",
        "status",
        "blocking_issue",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(audit.columns))
    if missing_columns:
        return [f"Release reproducibility audit missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    observed_checks = set(audit["check_id"].dropna().astype(str))
    for check_id in sorted(REQUIRED_RELEASE_READINESS_CHECKS.difference(observed_checks)):
        errors.append(f"Missing release reproducibility check: {check_id}")

    duplicates = audit[audit.duplicated(subset=["check_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate release reproducibility check: {_registry_field(duplicate_row, 'check_id')}"
        )

    allowed_statuses = {"blocked_missing_inputs", "ready", "ready_partial"}
    for row_number, record in enumerate(audit.to_dict("records"), start=2):
        check_id = _registry_field(record, "check_id") or f"row {row_number}"
        for column in required_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on release reproducibility row {row_number}")

        status = _registry_field(record, "status")
        if status and status not in allowed_statuses:
            errors.append(
                f"Unexpected status on release reproducibility row {row_number}: {status}"
            )

        blocking_issue = _registry_field(record, "blocking_issue")
        if status == "blocked_missing_inputs" and blocking_issue in {"", "none"}:
            errors.append(f"Blocked release reproducibility row {check_id} must name a blocker")
        if status == "ready" and blocking_issue != "none":
            errors.append(f"Ready release reproducibility row {check_id} must not name a blocker")

        for artifact in _registry_field(record, "input_artifacts").split(";"):
            artifact_path = Path(artifact)
            if artifact_path.is_absolute() or ".." in artifact_path.parts:
                errors.append(f"Unsafe input artifact on release reproducibility row {check_id}")
                continue
            if not (root / artifact_path).exists():
                errors.append(
                    f"Missing input artifact on release reproducibility row {check_id}: {artifact}"
                )

    requirement_path = root / "requirements-release.txt"
    if not requirement_path.is_file():
        errors.append("Missing requirements-release.txt")
    else:
        for line_number, line in enumerate(
            requirement_path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "==" not in stripped:
                errors.append(f"Unpinned release requirement on line {line_number}: {stripped}")

    return errors


def validate_submission_package(
    manifest_path: Path,
    root: Path,
) -> list[str]:
    """Return validation errors for the bounded submission package manifest."""
    if not isinstance(manifest_path, Path):
        raise TypeError("manifest_path must be pathlib.Path")
    if not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")

    package = pd.read_csv(manifest_path, dtype=str)
    required_columns = {
        "item_id",
        "artifact_path",
        "artifact_role",
        "required_for_submission",
        "current_status",
        "blocking_issue",
        "validation_gate",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(package.columns))
    if missing_columns:
        return [f"Submission package manifest missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    observed_items = set(package["item_id"].dropna().astype(str))
    for item_id in sorted(REQUIRED_SUBMISSION_PACKAGE_ITEMS.difference(observed_items)):
        errors.append(f"Missing submission package item: {item_id}")

    duplicates = package[package.duplicated(subset=["item_id"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate submission package item: {_registry_field(duplicate_row, 'item_id')}"
        )

    allowed_statuses = {"partial_bounded", "ready"}
    required_phrases = {
        root / "paper" / "data_code_availability.md": {
            "bounded research snapshot",
            "evidence/article_evidence.csv",
            "evidence/data_quality_registry.csv",
        },
        root / "paper" / "reviewer_methods_appendix.md": {
            "definitions",
            "accounting perimeters",
            "robustness variants",
            "current limitations",
        },
        root / "docs" / "replication_guide.md": {
            "make quality",
            "clean sequential notebook",
            "data/processed/submission_package_manifest.csv",
        },
    }

    for row_number, record in enumerate(package.to_dict("records"), start=2):
        item_id = _registry_field(record, "item_id") or f"row {row_number}"
        for column in required_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on submission package row {row_number}")

        artifact = Path(_registry_field(record, "artifact_path"))
        if artifact.is_absolute() or ".." in artifact.parts:
            errors.append(f"Unsafe artifact path on submission package row {item_id}")
            continue
        if not (root / artifact).is_file():
            errors.append(f"Missing submission package artifact for {item_id}: {artifact}")

        current_status = _registry_field(record, "current_status")
        if current_status and current_status not in allowed_statuses:
            errors.append(
                f"Unexpected submission package status on row {row_number}: {current_status}"
            )

        required_for_submission = _registry_field(record, "required_for_submission")
        if required_for_submission != "yes":
            errors.append(f"Submission package row {item_id} must be required for submission")

        blocking_issue = _registry_field(record, "blocking_issue")
        if current_status == "ready" and blocking_issue != "none":
            errors.append(f"Ready submission package row {item_id} must not name a blocker")
        if current_status == "partial_bounded" and blocking_issue in {"", "none"}:
            errors.append(f"Partial submission package row {item_id} must name a blocker")

    for artifact_path, phrases in required_phrases.items():
        if not artifact_path.is_file():
            continue
        text = artifact_path.read_text(encoding="utf-8").lower()
        for phrase in phrases:
            if phrase.lower() not in text:
                errors.append(
                    f"Submission package artifact {artifact_path.relative_to(root)} "
                    f"missing phrase: {phrase}"
                )

    return errors


def validate_claim_language_audit(
    audit_path: Path,
    manuscript_path: Path,
) -> list[str]:
    """Return validation errors for the manuscript loaded-language audit."""
    if not isinstance(audit_path, Path):
        raise TypeError("audit_path must be pathlib.Path")
    if not isinstance(manuscript_path, Path):
        raise TypeError("manuscript_path must be pathlib.Path")

    audit = pd.read_csv(audit_path, dtype=str)
    manuscript = manuscript_path.read_text(encoding="utf-8").lower()
    required_columns = {
        "term",
        "occurrence_count",
        "concept_mapping",
        "boundary_status",
        "claim_ids",
        "evidence_ids",
        "allowed_context",
        "prohibited_inference",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(audit.columns))
    if missing_columns:
        return [f"Claim language audit missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    observed_terms = set(audit["term"].dropna().astype(str))
    for term in sorted(REQUIRED_CLAIM_LANGUAGE_TERMS.difference(observed_terms)):
        errors.append(f"Missing claim language audit term: {term}")

    duplicates = audit[audit.duplicated(subset=["term"], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(
            f"Duplicate claim language audit term: {_registry_field(duplicate_row, 'term')}"
        )

    allowed_statuses = {"blocked_absent", "blocked_negated", "bounded_use"}
    for row_number, record in enumerate(audit.to_dict("records"), start=2):
        term = _registry_field(record, "term") or f"row {row_number}"
        for column in required_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on claim language audit row {row_number}")

        status = _registry_field(record, "boundary_status")
        if status and status not in allowed_statuses:
            errors.append(f"Unexpected claim language status on row {row_number}: {status}")

        count_text = _registry_field(record, "occurrence_count")
        try:
            recorded_count = int(count_text)
        except ValueError:
            errors.append(f"Claim language audit term {term} has noninteger occurrence_count")
            continue
        actual_count = len(re.findall(rf"(?<![a-z]){re.escape(term.lower())}(?![a-z])", manuscript))
        if recorded_count != actual_count:
            errors.append(
                f"Claim language audit term {term} count mismatch: "
                f"recorded {recorded_count}, actual {actual_count}"
            )

        if recorded_count > 0 and status == "blocked_absent":
            errors.append(f"Present claim language term {term} cannot be blocked_absent")
        if recorded_count == 0 and status != "blocked_absent":
            errors.append(f"Absent claim language term {term} must be blocked_absent")
        if recorded_count > 0 and _registry_field(record, "claim_ids") == "not_applicable":
            errors.append(f"Present claim language term {term} must map to a claim")
        if recorded_count > 0 and _registry_field(record, "evidence_ids") == "not_applicable":
            errors.append(f"Present claim language term {term} must map to evidence or blocker")

    unsupported_phrases = {
        "was diverted",
        "were diverted",
        "was underfunded",
        "bank-transfer subsidy.",
        "social security surplus is artificial",
        "proves sustainability",
    }
    for phrase in sorted(unsupported_phrases):
        if phrase in manuscript:
            errors.append(f"Manuscript contains unsupported loaded phrase: {phrase}")

    return errors


def _validate_evidence_level_artifact_registry(
    registry: pd.DataFrame,
    root: Path,
    *,
    registry_name: str,
    id_column: str,
    required_ids: frozenset[str] | None,
) -> list[str]:
    required_columns = {
        id_column,
        "title",
        "companion_csv",
        "source_datasets",
        "publication_status",
        "article_use_status",
        "notes",
    }
    if registry_name == "evidence figure registry":
        required_columns.add("primary_blocker")
    missing_columns = sorted(required_columns.difference(registry.columns))
    if missing_columns:
        return [f"{registry_name} missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    observed_ids = set(registry[id_column].dropna().astype(str))
    if required_ids is not None:
        for missing_id in sorted(required_ids.difference(observed_ids)):
            errors.append(f"Missing required article figure registry row: {missing_id}")
    for row_number, record in enumerate(registry.to_dict("records"), start=2):
        for column in required_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on {registry_name} row {row_number}")
        companion = _registry_field(record, "companion_csv")
        if companion and not (root / companion).is_file():
            errors.append(f"Missing companion CSV on {registry_name} row {row_number}: {companion}")
        publication_status = _registry_field(record, "publication_status")
        article_use_status = _registry_field(record, "article_use_status")
        if publication_status == "blocked" and article_use_status != "blocked_article_use":
            errors.append(f"Blocked artifact row {row_number} must block article use")
    return errors


def _validate_publication_registry(
    registry: pd.DataFrame,
    root: Path,
    *,
    id_column: str,
    required_ids: frozenset[str] | None,
    registry_name: str,
    companion_column: str,
    allowed_statuses: set[str],
    source_must_be_processed: bool,
) -> list[str]:
    required_columns = {
        id_column,
        "title",
        companion_column,
        "source_datasets",
        "publication_status",
        "notes",
    }
    if registry_name == "figure registry":
        required_columns.add("primary_blocker")
    missing_columns = sorted(required_columns.difference(registry.columns))
    if missing_columns:
        return [f"{registry_name} missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicates = registry[registry.duplicated(subset=[id_column], keep=False)]
    for _, duplicate_row in duplicates.iterrows():
        errors.append(f"Duplicate {registry_name} row: {_registry_field(duplicate_row, id_column)}")

    observed_ids = set(registry[id_column].dropna().astype(str))
    if required_ids is not None:
        for missing_id in sorted(required_ids.difference(observed_ids)):
            errors.append(f"Missing required publication figure: {missing_id}")
        for unexpected_id in sorted(observed_ids.difference(required_ids)):
            errors.append(f"Unexpected publication figure: {unexpected_id}")

    for row_number, record in enumerate(registry.to_dict("records"), start=2):
        artifact_id = _registry_field(record, id_column) or f"row {row_number}"
        for column in required_columns:
            if not _registry_field(record, column):
                errors.append(f"Missing {column} on {registry_name} row {row_number}")

        status = _registry_field(record, "publication_status")
        if status and status not in allowed_statuses:
            errors.append(
                f"Unexpected publication_status on {registry_name} row {row_number}: {status}"
            )

        companion = Path(_registry_field(record, companion_column))
        if companion.is_absolute() or ".." in companion.parts:
            errors.append(f"Unsafe companion path for {artifact_id}: {companion}")
            continue
        companion_path = root / companion
        if not companion_path.is_file():
            errors.append(f"Missing companion CSV for {artifact_id}: {companion}")
            continue
        errors.extend(_validate_publication_companion(companion_path, artifact_id, id_column))

        source_datasets = _registry_field(record, "source_datasets")
        if source_must_be_processed and status != "blocked":
            for source_dataset in source_datasets.split(";"):
                if not source_dataset.startswith("data/processed/"):
                    errors.append(f"Ready figure {artifact_id} must use processed source datasets")
                elif not (root / source_dataset).is_file():
                    errors.append(f"Ready figure {artifact_id} source is missing: {source_dataset}")
        if status == "blocked" and not _registry_field(record, "primary_blocker"):
            errors.append(f"Blocked figure {artifact_id} must name primary_blocker")
    return errors


def _validate_publication_companion(
    companion_path: Path,
    artifact_id: str,
    id_column: str,
) -> list[str]:
    companion = pd.read_csv(companion_path, dtype=str)
    if id_column not in companion.columns:
        return [f"Companion CSV for {artifact_id} missing {id_column}"]
    errors: list[str] = []
    companion_ids = set(companion[id_column].dropna().astype(str))
    if companion_ids != {artifact_id}:
        errors.append(f"Companion CSV for {artifact_id} has mismatched IDs")
    if "status" in companion.columns:
        has_value_column = "value" in companion.columns
        for row_number, record in enumerate(companion.to_dict("records"), start=2):
            status = _registry_field(record, "status")
            value = _registry_field(record, "value") if has_value_column else ""
            if status.startswith("ready") and not value:
                errors.append(f"Ready companion row {row_number} for {artifact_id} missing value")
            if status.startswith("blocked") and value:
                errors.append(
                    f"Blocked companion row {row_number} for {artifact_id} must not have value"
                )
    return errors


def validate_source_registry(registry_path: Path, root: Path) -> list[str]:
    """Return validation errors for source registry acquisition metadata."""
    if not isinstance(registry_path, Path):
        raise TypeError("registry_path must be pathlib.Path")
    if not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")

    if not registry_path.is_file():
        return [f"Missing source registry file: {registry_path.name}"]

    try:
        registry = pd.read_csv(registry_path, dtype=str)
    except Exception as exc:  # pragma: no cover - defensive parsing boundary
        return [f"Unreadable source registry: {exc}"]

    required_columns = {
        "source_id",
        "title",
        "institution",
        "source_type",
        "year",
        "url",
        "download_url",
        "retrieval_date",
        "reporting_period",
        "accounting_basis",
        "raw_path",
        "sha256",
        "status",
        "notes",
    }
    missing_columns = sorted(required_columns.difference(registry.columns))
    if missing_columns:
        return [f"Source registry missing columns: {', '.join(missing_columns)}"]

    errors: list[str] = []
    duplicated_ids = sorted(
        source_id
        for source_id in registry["source_id"].dropna().astype(str).unique()
        if (registry["source_id"].astype(str) == source_id).sum() > 1
    )
    for source_id in duplicated_ids:
        errors.append(f"Duplicate source_id in source registry: {source_id}")

    for row_number, (_, row) in enumerate(registry.iterrows(), start=2):
        source_id = _registry_field(row, "source_id") or f"row {row_number}"
        status = _registry_field(row, "status").lower()
        if status != "acquired":
            continue

        raw_path_value = _registry_field(row, "raw_path")
        expected_hash = _registry_field(row, "sha256").lower()
        if not raw_path_value:
            errors.append(f"Source {source_id} is acquired but raw_path is empty")
            continue
        if len(expected_hash) != 64 or any(
            char not in "0123456789abcdef" for char in expected_hash
        ):
            errors.append(f"Source {source_id} has invalid SHA-256 hash")
            continue

        candidate = Path(raw_path_value)
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append(f"Source {source_id} has unsafe raw_path: {raw_path_value}")
            continue

        raw_file = root / candidate
        if not raw_file.is_file():
            errors.append(f"Source {source_id} raw file is missing: {raw_path_value}")
            continue

        actual_hash = hashlib.sha256(raw_file.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(f"Source {source_id} checksum mismatch for {raw_path_value}")
    return errors


def validate_data_license_registry(
    license_path: Path,
    source_registry_path: Path,
) -> list[str]:
    """Return validation errors for source licensing and redistribution metadata."""
    if not isinstance(license_path, Path):
        raise TypeError("license_path must be pathlib.Path")
    if not isinstance(source_registry_path, Path):
        raise TypeError("source_registry_path must be pathlib.Path")

    licenses = pd.read_csv(license_path, dtype=str, keep_default_na=False)
    sources = pd.read_csv(source_registry_path, dtype=str, keep_default_na=False)
    missing_columns = sorted(DATA_LICENSE_REQUIRED_COLUMNS.difference(licenses.columns))
    if missing_columns:
        return [f"Data license registry missing columns: {', '.join(missing_columns)}"]

    source_ids = set(sources["source_id"])
    license_ids = set(licenses["source_id"])
    errors: list[str] = []
    for source_id in sorted(source_ids.difference(license_ids)):
        errors.append(f"Source missing data license row: {source_id}")
    for source_id in sorted(license_ids.difference(source_ids)):
        errors.append(f"Data license row references unknown source_id: {source_id}")

    duplicate_ids = sorted(
        licenses.loc[licenses["source_id"].duplicated(), "source_id"].dropna().unique()
    )
    for source_id in duplicate_ids:
        errors.append(f"Duplicate data license row: {source_id}")

    source_status_by_id = {
        str(row["source_id"]): str(row["status"]).strip().lower()
        for row in sources.to_dict("records")
    }
    raw_path_by_id = {
        str(row["source_id"]): str(row["raw_path"]).strip() for row in sources.to_dict("records")
    }

    for row in licenses.to_dict("records"):
        source_id = row["source_id"].strip()
        if not source_id:
            errors.append("Data license registry contains a row with empty source_id")
            continue
        for column in DATA_LICENSE_REQUIRED_COLUMNS:
            if not row[column].strip():
                errors.append(f"Data license row {source_id} has empty {column}")
        if row["access_status"] not in DATA_LICENSE_ACCESS_STATUSES:
            errors.append(
                f"Data license row {source_id} has invalid access_status: {row['access_status']}"
            )
        if row["redistribution_status"] not in DATA_LICENSE_REDISTRIBUTION_STATUSES:
            errors.append(
                f"Data license row {source_id} has invalid redistribution_status: "
                f"{row['redistribution_status']}"
            )

        source_status = source_status_by_id.get(source_id, "")
        raw_path = raw_path_by_id.get(source_id, "")
        if source_status == "acquired" and row["access_status"] != "acquired_public_download":
            errors.append(f"Acquired source {source_id} must use acquired_public_download")
        if source_status != "acquired" and raw_path:
            errors.append(f"Non-acquired source {source_id} must not have raw release path")
        if row["redistribution_status"] == "not_acquired_no_redistribution" and raw_path:
            errors.append(f"Acquired source {source_id} cannot be marked not acquired")
        if (
            row["redistribution_status"] == "permission_unclear_do_not_redistribute"
            and raw_path
            and "exclude_raw_from_public_release" not in row["repository_action"]
        ):
            errors.append(
                f"Unclear redistribution source {source_id} must exclude raw file "
                "from public release"
            )
        if (
            row["redistribution_status"] == "allowed_with_attribution"
            and "cite_source" not in row["repository_action"]
        ):
            errors.append(f"Redistributable source {source_id} must require source citation")
        if "source_registry" not in row["clean_room_instruction"]:
            errors.append(f"Data license row {source_id} must reference source_registry")
        if raw_path and "sha256" not in row["archival_reference"].lower():
            errors.append(f"Acquired source {source_id} must preserve SHA-256 archival reference")

    return errors


def _registry_field(row: Any, column: str) -> str:
    value = row[column]
    if pd.isna(value):
        return ""
    return str(value).strip()


def validate_manifest(manifest_path: Path, root: Path | None = None) -> list[str]:
    """Return validation errors for files listed in a sha256sum-style manifest."""
    if not isinstance(manifest_path, Path):
        raise TypeError("manifest_path must be pathlib.Path")
    if root is not None and not isinstance(root, Path):
        raise TypeError("root must be pathlib.Path")

    if not manifest_path.is_file():
        return [f"Missing manifest file: {manifest_path.name}"]

    root_dir = root if root is not None else manifest_path.parent
    errors: list[str] = []
    for line_number, line in enumerate(
        manifest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            expected_hash, relative_path = line.split(maxsplit=1)
        except ValueError:
            errors.append(f"Malformed manifest line {line_number}")
            continue
        if len(expected_hash) != 64 or any(
            char not in "0123456789abcdef" for char in expected_hash
        ):
            errors.append(f"Invalid SHA-256 hash on manifest line {line_number}")
            continue

        candidate = Path(relative_path.removeprefix("./"))
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append(f"Unsafe manifest path on line {line_number}: {relative_path}")
            continue

        path = root_dir / candidate
        if not path.is_file():
            errors.append(f"Missing manifest entry target: {relative_path}")
            continue

        actual_hash = hashlib.sha256(manifest_bytes(path)).hexdigest()
        if actual_hash != expected_hash:
            errors.append(f"Checksum mismatch for {relative_path}")
    return errors


def manifest_bytes(path: Path) -> bytes:
    """Return stable bytes for repository manifest hashing."""
    data = path.read_bytes()
    if path.name in TEXT_MANIFEST_NAMES or path.suffix.lower() in TEXT_MANIFEST_SUFFIXES:
        return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return data


def validate_zenodo_metadata(path: Path) -> list[str]:
    """Return validation errors for the repository Zenodo metadata file."""
    if not isinstance(path, Path):
        raise TypeError("path must be pathlib.Path")
    if not path.is_file():
        return ["Missing Zenodo metadata file: .zenodo.json"]

    try:
        metadata: Any = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid Zenodo JSON: {exc.msg} at line {exc.lineno}"]

    if not isinstance(metadata, dict):
        return ["Zenodo metadata must be a JSON object"]

    errors: list[str] = []
    required_string_fields = ("title", "upload_type", "description", "version", "license")
    for field in required_string_fields:
        if not isinstance(metadata.get(field), str) or not metadata[field].strip():
            errors.append(f"Missing or empty Zenodo field: {field}")

    creators = metadata.get("creators")
    if not isinstance(creators, list) or not creators:
        errors.append("Zenodo metadata requires at least one creator")
    else:
        for index, creator in enumerate(creators, start=1):
            if not isinstance(creator, dict):
                errors.append(f"Zenodo creator {index} must be an object")
                continue
            if not isinstance(creator.get("name"), str) or not creator["name"].strip():
                errors.append(f"Zenodo creator {index} is missing a name")

    keywords = metadata.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list) or any(not isinstance(item, str) for item in keywords)
    ):
        errors.append("Zenodo keywords must be a list of strings")

    return errors
