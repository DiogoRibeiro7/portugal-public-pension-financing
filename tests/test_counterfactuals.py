from pathlib import Path

import pytest

from portugal_pensions.counterfactuals import (
    compound_reserve,
    funding_substitution,
    validate_public_worker_reallocation,
)


def test_compound_reserve() -> None:
    path = compound_reserve([100.0, 100.0], [0.10, 0.10])
    assert path == pytest.approx([110.0, 231.0])


def test_funding_substitution_does_not_create_extra_cash() -> None:
    employer, state = funding_substitution(100.0, 40.0)
    assert employer + state == pytest.approx(100.0)


def test_repository_public_worker_reallocation_files_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_public_worker_reallocation(
            str(root / "data" / "processed" / "public_worker_rgss_cohorts.csv"),
            str(root / "data" / "processed" / "public_worker_rgss_contributions_2006_2025.csv"),
        )
        == []
    )


def test_public_worker_reallocation_requires_full_year_coverage(tmp_path: Path) -> None:
    cohorts = tmp_path / "cohorts.csv"
    contributions = tmp_path / "contributions.csv"
    cohorts.write_text(
        "year,cohort,lower,central,upper,unit,source_ids,status,notes\n"
        "2006,cohort,,,,workers,SRC,blocked,missing\n",
        encoding="utf-8",
    )
    contributions.write_text(
        "year,employee_contributions_lower,employee_contributions_central,"
        "employee_contributions_upper,employer_contributions_lower,"
        "employer_contributions_central,employer_contributions_upper,unit,source_ids,"
        "observation_type,status,notes\n"
        "2006,,,,,,,EUR_million,SRC,mechanical_reallocation,blocked,missing\n",
        encoding="utf-8",
    )

    errors = validate_public_worker_reallocation(str(cohorts), str(contributions))
    assert "public worker cohort table must cover every year from 2006 to 2025" in errors
