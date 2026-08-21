from datetime import date
from pathlib import Path

import pytest

from portugal_pensions.legal import (
    counterfactual_rate_gap,
    employer_perimeter_at,
    rgss_benchmark_at,
    statutory_liability,
    validate_employer_perimeter_registry,
    validate_legal_contribution_registry,
    validate_rgss_rate_decomposition,
)


def test_statutory_liability() -> None:
    assert statutory_liability(1_000.0, 0.10) == pytest.approx(100.0)


def test_rate_must_be_fraction() -> None:
    with pytest.raises(ValueError):
        statutory_liability(1_000.0, 1.1)


def test_repository_legal_contribution_registry_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_legal_contribution_registry(
            str(root / "evidence" / "legal_contribution_registry.csv"),
            str(root / "evidence" / "source_registry.csv"),
        )
        == []
    )


def test_repository_employer_perimeter_registry_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_employer_perimeter_registry(
            str(root / "evidence" / "employer_perimeter_registry.csv"),
            str(root / "evidence" / "source_registry.csv"),
            str(root / "evidence" / "legal_contribution_registry.csv"),
        )
        == []
    )


def test_repository_rgss_rate_decomposition_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_rgss_rate_decomposition(
            str(root / "evidence" / "rgss_rate_decomposition.csv"),
            str(root / "evidence" / "source_registry.csv"),
        )
        == []
    )


def test_rgss_pension_benchmark_is_labeled_counterfactual() -> None:
    root = Path(__file__).resolve().parents[1]
    benchmark = rgss_benchmark_at(
        str(root / "evidence" / "rgss_rate_decomposition.csv"),
        "RGSS_PENSION_RISK_2012",
        date(2012, 12, 31),
        rate_column="pension_risk_rate",
    )

    assert benchmark.rate == pytest.approx(0.2694)
    assert benchmark.legal_status == "economic_counterfactual"
    assert "not legal debt" in benchmark.notes


def test_counterfactual_rate_gap_uses_labeled_rate_arithmetic() -> None:
    assert counterfactual_rate_gap(
        contribution_base=1_000.0,
        observed_rate=0.2600,
        benchmark_rate=0.2694,
    ) == pytest.approx(9.4)


def test_employer_perimeter_lookup_returns_active_row() -> None:
    root = Path(__file__).resolve().parents[1]
    row = employer_perimeter_at(
        str(root / "evidence" / "employer_perimeter_registry.csv"),
        "entities_first_covered_2009",
        date(2010, 1, 1),
    )

    assert row["cga_contribution_regime"] == "entities_first_covered_2009"
    assert row["national_accounts_sector"] == "sector_varies_by_entity_and_year"


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

    assert (
        "Overlapping legal contribution intervals for class"
        in validate_legal_contribution_registry(str(registry))
    )


def test_legal_contribution_registry_rejects_unknown_source_id(tmp_path: Path) -> None:
    registry = tmp_path / "legal_contribution_registry.csv"
    registry.write_text(
        "effective_from,effective_to,employer_class,worker_rate_retirement,"
        "worker_rate_survivor,worker_rate_total,employer_rate_retirement,"
        "employer_rate_survivor,employer_rate_total,contribution_base_definition,"
        "covered_risks,source_id,article,status,notes\n"
        "2014-01-01,,central_state_integrated_services,0.08,0.03,0.11,0.20,"
        "0.0375,0.2375,remuneration subject to CGA quota,retirement;survivor,"
        "MISSING,article,current_consolidated_rule,notes\n",
        encoding="utf-8",
    )
    sources = tmp_path / "source_registry.csv"
    sources.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "KNOWN,Source,Institution,official,2026,https://example.test,"
        "https://example.test,2026-08-21,2026,basis,,,registered,notes\n",
        encoding="utf-8",
    )

    errors = validate_legal_contribution_registry(str(registry), str(sources))
    assert "Unknown legal contribution source_id on row 2: MISSING" in errors


def test_employer_perimeter_registry_rejects_collapsed_legal_and_statistical_sector(
    tmp_path: Path,
) -> None:
    sources = tmp_path / "source_registry.csv"
    sources.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,Source,Institution,official,2026,https://example.test,"
        "https://example.test,2026-08-21,2026,basis,,,registered,notes\n",
        encoding="utf-8",
    )
    legal = tmp_path / "legal_contribution_registry.csv"
    legal.write_text(
        "effective_from,effective_to,employer_class,worker_rate_retirement,"
        "worker_rate_survivor,worker_rate_total,employer_rate_retirement,"
        "employer_rate_survivor,employer_rate_total,contribution_base_definition,"
        "covered_risks,source_id,article,status,notes\n"
        "2014-01-01,,central_state_integrated_services,0.08,0.03,0.11,0.20,"
        "0.0375,0.2375,remuneration subject to CGA quota,retirement;survivor,"
        "SRC,article,current_consolidated_rule,notes\n",
        encoding="utf-8",
    )
    perimeter = tmp_path / "employer_perimeter_registry.csv"
    perimeter.write_text(
        "employer_class,valid_from,valid_to,legal_regime,statistical_sector,"
        "national_accounts_sector,cga_contribution_regime,rgss_new_entrants_rule,"
        "source_id,status,notes\n"
        "central_state_integrated_services,2014-01-01,,same,same,central,"
        "central_state_integrated_services,new entrants enter RGSS,SRC,"
        "official_summary_mapping,notes\n",
        encoding="utf-8",
    )

    errors = validate_employer_perimeter_registry(str(perimeter), str(sources), str(legal))
    assert "Employer perimeter row 2 collapses legal and statistical sectors" in errors


def test_rgss_rate_decomposition_rejects_pension_benchmark_without_debt_guard(
    tmp_path: Path,
) -> None:
    sources = tmp_path / "source_registry.csv"
    sources.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,Source,Institution,official,2012,https://example.test,"
        "https://example.test,2026-08-21,2012,basis,,,registered,notes\n",
        encoding="utf-8",
    )
    registry = tmp_path / "rgss_rate_decomposition.csv"
    registry.write_text(
        "scenario_id,valid_from,valid_to,rate_owner,benchmark_kind,worker_rate,"
        "employer_rate,total_rate,pension_risk_rate,broad_social_protection_rate,"
        "other_risk_rate,covered_risks,excluded_risks,public_employer_risk_mapping,"
        "legal_status,source_id,status,notes\n"
        "RGSS_BROAD_2012,2012-01-01,2012-12-31,RGSS,broad_social_protection,"
        "0.1100,0.2375,0.3475,,0.3475,,all,not_applicable,mapping,"
        "actual_rgss_rate_not_cga_requirement,SRC,official_bounded_extract,"
        "Full RGSS rate is broad social-protection and not pension-only.\n"
        "RGSS_PENSION_RISK_2012,2012-01-01,2012-12-31,RGSS,"
        "comparable_pension_risk,,,0.2694,0.2694,,,pension,other,mapping,"
        "actual_rgss_rate_not_cga_requirement,SRC,official_bounded_extract,"
        "economic benchmark\n"
        "PUBLIC_EMPLOYER_DIRECT_RISK_MAPPING_BLOCKER,2006-01-01,2025-12-31,"
        "public_employers,direct_risk_mapping,,,,,,,,other,blocked,"
        "unresolved_source_requirement,SRC,blocked_missing_source_extraction,blocked\n"
        "RGSS_HISTORICAL_DECOMPOSITION_BLOCKER,1977-01-01,2025-12-31,RGSS,"
        "historical_series_blocker,,,,,,,,all,blocked,unresolved_source_requirement,"
        "SRC,blocked_missing_source_extraction,blocked\n",
        encoding="utf-8",
    )

    errors = validate_rgss_rate_decomposition(str(registry), str(sources))
    assert (
        "Comparable pension-risk row RGSS_PENSION_RISK_2012 must be an economic benchmark" in errors
    )
    assert "Comparable pension-risk row RGSS_PENSION_RISK_2012 must state not legal debt" in errors
