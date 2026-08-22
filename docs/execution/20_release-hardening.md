# Harden release workflow

Instruction file: `prompts/20_release_reproducibility.md`
Date: 2026-08-19
Updated: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Checked the current source registry, publication artifact registry, manifest gate, manuscript
  evidence gate, CI quality gate, notebook inventory, and release metadata.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.
- Added `data/processed/release_reproducibility_audit.csv` as the machine-readable readiness
  ledger.
- Added `docs/reproducibility_report.md` and expanded `docs/replication_guide.md`.
- Added `requirements-release.txt` for pinned direct dependencies used by the readiness snapshot.
- Added validation and tests for release-readiness audit coverage and pinned requirements.
- Added a compiled-manuscript PDF release gate tying `paper/manuscript.pdf` to
  `paper/manuscript.tex` and `MANIFEST.sha256`.

## Result

Recorded current release readiness and remaining blockers. The repository passes the quality,
manifest, Zenodo, source-hash, publication-artifact, article-evidence, and manuscript gates, but it
is not yet a final public-report release because the manuscript remains bounded, clean sequential
notebook execution and several primary-source inputs remain blocked.

## Current Stop Condition

Completion beyond this record requires a clean archived sequential notebook run plus the registered
primary sources and deterministic extraction chain needed by the task. Until those inputs exist,
the readiness audit must remain partial under the repository evidence rules.

## Validation

This branch ran repository quality checks after regenerating `MANIFEST.sha256`.
