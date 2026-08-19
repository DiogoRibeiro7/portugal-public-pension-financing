from pathlib import Path

import pytest

from portugal_pensions.legal import statutory_liability, validate_legal_contribution_registry


def test_statutory_liability() -> None:
    assert statutory_liability(1_000.0, 0.10) == pytest.approx(100.0)


def test_rate_must_be_fraction() -> None:
    with pytest.raises(ValueError):
        statutory_liability(1_000.0, 1.1)


def test_repository_legal_contribution_registry_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_legal_contribution_registry(
            str(root / "evidence" / "legal_contribution_registry.csv")
        )
        == []
    )


def test_legal_contribution_registry_rejects_overlapping_intervals(tmp_path: Path) -> None:
    registry = tmp_path / "legal_contribution_registry.csv"
    registry.write_text(
        "effective_from,effective_to,employer_class,worker_rate_retirement,"
        "worker_rate_survivor,worker_rate_total,employer_rate_retirement,"
        "employer_rate_survivor,employer_rate_total,contribution_base_definition,"
        "covered_risks,source_id,article,status,notes\n"
        "2020-01-01,2020-12-31,class,0.08,0.03,0.11,0.20,0.0375,0.2375,"
        "base,retirement;survivor,SRC,article,verified,notes\n"
        "2020-06-01,2021-12-31,class,0.08,0.03,0.11,0.20,0.0375,0.2375,"
        "base,retirement;survivor,SRC,article,verified,notes\n",
        encoding="utf-8",
    )

    assert validate_legal_contribution_registry(str(registry)) == [
        "Overlapping legal contribution intervals for class"
    ]
