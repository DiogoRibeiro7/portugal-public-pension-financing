"""Validation of research registries and evidence contracts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from .accounting import (
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
