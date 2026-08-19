from pathlib import Path

from portugal_pensions.validation import validate_evidence_directory, validate_manifest


def test_repository_evidence_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_evidence_directory(root / "evidence") == []


def test_manifest_validation_accepts_matching_hash(tmp_path: Path) -> None:
    payload = tmp_path / "payload.txt"
    payload.write_bytes(b"reproducible\n")
    manifest = tmp_path / "MANIFEST.sha256"
    manifest.write_text(
        "9eea221f83299a3ebea16d547cb0f1cbbaace6be5c925cd9f0ccfcd1b6549c67  ./payload.txt\n",
        encoding="utf-8",
    )

    assert validate_manifest(manifest, tmp_path) == []


def test_manifest_validation_reports_mismatch(tmp_path: Path) -> None:
    payload = tmp_path / "payload.txt"
    payload.write_bytes(b"changed\n")
    manifest = tmp_path / "MANIFEST.sha256"
    manifest.write_text(f"{'0' * 64}  ./payload.txt\n", encoding="utf-8")

    assert validate_manifest(manifest, tmp_path) == ["Checksum mismatch for ./payload.txt"]
