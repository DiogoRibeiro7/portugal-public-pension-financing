from pathlib import Path

from portugal_pensions.validation import validate_evidence_directory


def test_repository_evidence_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_evidence_directory(root / "evidence") == []
