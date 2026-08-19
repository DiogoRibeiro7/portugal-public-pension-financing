from pathlib import Path

from portugal_pensions.validation import (
    validate_evidence_directory,
    validate_manifest,
    validate_zenodo_metadata,
)


def test_repository_evidence_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_evidence_directory(root / "evidence") == []


def test_repository_zenodo_metadata_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_zenodo_metadata(root / ".zenodo.json") == []


def test_manifest_validation_accepts_matching_hash(tmp_path: Path) -> None:
    payload = tmp_path / "payload.txt"
    payload.write_bytes(b"reproducible\n")
    manifest = tmp_path / "MANIFEST.sha256"
    manifest.write_text(
        "9eea221f83299a3ebea16d547cb0f1cbbaace6be5c925cd9f0ccfcd1b6549c67  ./payload.txt\n",
        encoding="utf-8",
    )

    assert validate_manifest(manifest, tmp_path) == []


def test_manifest_validation_normalizes_text_line_endings(tmp_path: Path) -> None:
    payload = tmp_path / "payload.csv"
    payload.write_bytes(b"column\r\nvalue\r\n")
    manifest = tmp_path / "MANIFEST.sha256"
    manifest.write_text(
        "026cca97661612db545eba77bd301821146b2029d14d4082890565d9efef91ea  ./payload.csv\n",
        encoding="utf-8",
    )

    assert validate_manifest(manifest, tmp_path) == []


def test_manifest_validation_reports_mismatch(tmp_path: Path) -> None:
    payload = tmp_path / "payload.txt"
    payload.write_bytes(b"changed\n")
    manifest = tmp_path / "MANIFEST.sha256"
    manifest.write_text(f"{'0' * 64}  ./payload.txt\n", encoding="utf-8")

    assert validate_manifest(manifest, tmp_path) == ["Checksum mismatch for ./payload.txt"]


def test_zenodo_metadata_requires_creator(tmp_path: Path) -> None:
    metadata = tmp_path / ".zenodo.json"
    metadata.write_text(
        '{"title": "Project", "upload_type": "software", "description": "Test", '
        '"version": "0.1.0", "license": "mit", "creators": []}',
        encoding="utf-8",
    )

    assert validate_zenodo_metadata(metadata) == ["Zenodo metadata requires at least one creator"]
