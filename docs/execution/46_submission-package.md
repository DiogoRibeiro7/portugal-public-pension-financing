# Prepare submission package

Instruction file: `prompts/46_journal_submission_replication_package.md`
Date: 2026-08-19
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Checked the release-readiness audit, replication guide, manuscript, article evidence, manifest,
  and data-quality blockers.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.
- Added `paper/data_code_availability.md`.
- Added `paper/reviewer_methods_appendix.md`.
- Added `data/processed/submission_package_manifest.csv`.
- Expanded `docs/replication_guide.md` with the current package contents and certified gate.
- Added validation and tests for the bounded submission package.

## Result

Prepared a bounded submission package scaffold. It is suitable for reviewer orientation and
independent reproduction of the currently gated article-evidence claims, but it is not a final
journal submission package because release-readiness blockers remain open.

## Current Stop Condition

Completion beyond this record requires the registered primary sources, deterministic extraction
chain, clean sequential notebook execution log, and final manuscript inputs needed by the task.
Until those inputs exist, the submission package remains partial under the repository evidence
rules.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` after regenerating `MANIFEST.sha256`.
