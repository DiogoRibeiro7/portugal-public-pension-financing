"""Validation of research registries and evidence contracts."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

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
    return errors


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

        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(f"Checksum mismatch for {relative_path}")
    return errors
