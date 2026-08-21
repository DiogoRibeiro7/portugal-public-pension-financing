"""Validation of research registries and evidence contracts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from .accounting import (
    validate_cga_closed_scheme_decomposition,
    validate_cga_financing_ledger,
    validate_employee_remittance_audit,
    validate_employer_contribution_audit,
    validate_pension_flow_of_funds,
)
from .banking import (
    validate_bank_asset_liability_outputs,
    validate_bank_benefit_risk_distribution,
    validate_bank_esa_treatment_bridge,
    validate_bank_pension_cost_2012,
    validate_bank_pension_transfer_registry,
    validate_bank_special_regime_annual,
    validate_bank_transfer_debt_financing_effects,
    validate_bpn_2012_pension_transfer,
)
from .counterfactuals import (
    validate_counterfactual_financing_regimes,
    validate_public_worker_reallocation,
)
from .legal import validate_legal_contribution_registry

REQUIRED_EVIDENCE_FILES: tuple[str, ...] = (
    "source_registry.csv",
    "claim_registry.csv",
    "legal_contribution_registry.csv",
    "bank_pension_transfer_registry.csv",
    "bank_special_regime_annual.csv",
    "reconciliation_log.csv",
    "data_quality_registry.csv",
    "counterfactual_registry.csv",
    "article_evidence.csv",
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
    if (evidence_dir / "legal_contribution_registry.csv").is_file():
        errors.extend(
            validate_legal_contribution_registry(
                str(evidence_dir / "legal_contribution_registry.csv")
            )
        )
    if (evidence_dir / "bank_pension_transfer_registry.csv").is_file():
        errors.extend(
            validate_bank_pension_transfer_registry(
                str(evidence_dir / "bank_pension_transfer_registry.csv")
            )
        )
    if (evidence_dir / "bank_special_regime_annual.csv").is_file():
        errors.extend(
            validate_bank_special_regime_annual(
                str(evidence_dir / "bank_special_regime_annual.csv")
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
        errors.extend(validate_cga_financing_ledger(str(cga_ledger)))
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
        errors.extend(validate_employee_remittance_audit(str(employee_remittance)))
    employer_contribution = (
        evidence_dir.parent / "data" / "processed" / "employer_contribution_audit.csv"
    )
    if employer_contribution.is_file():
        errors.extend(validate_employer_contribution_audit(str(employer_contribution)))
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
