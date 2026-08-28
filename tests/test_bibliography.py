"""Tests for bibliography generation and manuscript-section pointer integrity."""

from __future__ import annotations

from pathlib import Path

from portugal_pensions.bibliography import (
    build_bibliography,
    cite_key,
    validate_bibliography,
    validate_manuscript_citations,
    write_bibliography,
)
from portugal_pensions.validation import validate_manuscript_section_pointers

LITERATURE_HEADER = "reference_id,title,year,authors,venue,source_category,source_url\n"
LITERATURE_ROW = (
    "LIT_EXAMPLE_2020_STUDY,An Example Study,2020,Ana Example and Bruno Case,"
    "Journal of Tests,academic_literature,https://example.test/study.pdf\n"
)


def _literature_map(tmp_path: Path, extra: str = "") -> Path:
    path = tmp_path / "literature_map.csv"
    path.write_text(LITERATURE_HEADER + LITERATURE_ROW + extra, encoding="utf-8")
    return path


def test_cite_key_strips_registry_prefix() -> None:
    assert cite_key("LIT_EXAMPLE_2020_STUDY") == "example_2020_study"


def test_build_bibliography_renders_registered_entry(tmp_path: Path) -> None:
    rendered = build_bibliography(_literature_map(tmp_path))

    assert "@article{example_2020_study," in rendered
    assert "author      = {Ana Example and Bruno Case}," in rendered
    assert "journal     = {Journal of Tests}," in rendered


def test_build_bibliography_marks_unknown_year(tmp_path: Path) -> None:
    extra = (
        "LIT_UNDATED_PAPER,Undated Paper,unknown,Carla Author,Conference,"
        "academic_literature,https://example.test/undated.pdf\n"
    )
    rendered = build_bibliography(_literature_map(tmp_path, extra))

    assert "year        = {n.d.}," in rendered


def test_validate_bibliography_detects_stale_file(tmp_path: Path) -> None:
    literature = _literature_map(tmp_path)
    bibliography = tmp_path / "references.bib"
    write_bibliography(literature, bibliography)
    assert validate_bibliography(bibliography, literature) == []

    bibliography.write_text("@article{stale,}\n", encoding="utf-8")

    assert validate_bibliography(bibliography, literature) == [
        "Generated bibliography is stale: regenerate with "
        "`python -m portugal_pensions.cli build-bibliography`"
    ]


def test_validate_manuscript_citations_rejects_unknown_key(tmp_path: Path) -> None:
    literature = _literature_map(tmp_path)
    bibliography = tmp_path / "references.bib"
    write_bibliography(literature, bibliography)
    manuscript = tmp_path / "manuscript.tex"
    manuscript.write_text(
        r"\citet{example_2020_study} and \citep{missing_2019_paper}.",
        encoding="utf-8",
    )

    assert validate_manuscript_citations(manuscript, bibliography) == [
        "Manuscript cites unknown bibliography key: missing_2019_paper"
    ]


def _boundaries(tmp_path: Path) -> Path:
    path = tmp_path / "manuscript_section_boundaries.csv"
    path.write_text("section_id\nMS_CGA\nMS_BANK\n", encoding="utf-8")
    return path


def test_section_pointers_reject_positional_integer(tmp_path: Path) -> None:
    article = tmp_path / "article_evidence.csv"
    article.write_text("evidence_id,manuscript_section\nAE_ONE,8\n", encoding="utf-8")
    claims = tmp_path / "claim_registry.csv"
    claims.write_text("claim_id,manuscript_section\nC_ONE,MS_BANK\n", encoding="utf-8")

    assert validate_manuscript_section_pointers(article, claims, _boundaries(tmp_path)) == [
        "article_evidence.csv row AE_ONE names unknown manuscript section 8"
    ]


def test_section_pointers_accept_cross_cutting_sentinel(tmp_path: Path) -> None:
    article = tmp_path / "article_evidence.csv"
    article.write_text("evidence_id,manuscript_section\nAE_ONE,MS_CGA\n", encoding="utf-8")
    claims = tmp_path / "claim_registry.csv"
    claims.write_text("claim_id,manuscript_section\nC_ONE,all\n", encoding="utf-8")

    assert validate_manuscript_section_pointers(article, claims, _boundaries(tmp_path)) == []
