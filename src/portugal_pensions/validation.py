"""Validation of research registries and evidence contracts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

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
