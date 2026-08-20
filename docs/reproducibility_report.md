# Reproducibility report

Date: 2026-08-20

This report records release readiness for the current bounded research state. It is not a
publication release, tag, or DOI snapshot.

## Passing gates

- `make quality` passes locally.
- Raw-source hashes for acquired sources validate through `evidence/source_registry.csv`.
- Figure and table registries have companion CSV paths and explicit blockers for incomplete
  artifacts.
- The manuscript source is checked against `evidence/article_evidence.csv`.
- `MANIFEST.sha256` is the current archive checksum manifest.

## Blocked gates

- The notebooks have not been archived as a clean sequential execution run.
- Several official sources remain registered but not acquired as immutable raw files.
- Missing CGA component ledgers, payroll withholding records, bank-level transfer schedules,
  actuarial cash-flow paths, post-2012 financing series, and combined-balance inputs prevent a
  full public-report release.

## Environment

Use `requirements-release.txt` for the current pinned readiness snapshot. Normal development still
uses `pyproject.toml` ranges so CI can test supported Python versions.

## Archive manifest

`MANIFEST.sha256` records checksums for tracked files in this source state using normalized text
line endings for text files. Regenerate it after any source, evidence, documentation, or metadata
change and validate it before tagging a future release.
