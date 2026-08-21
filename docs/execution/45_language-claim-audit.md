# Audit claim language

Instruction file: `prompts/45_manuscript_definitions_causal_language_and_claim_audit.md`
Date: 2026-08-19
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Checked the current manuscript, article evidence, claim registry, and manuscript evidence gate.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.
- Added `data/processed/manuscript_claim_language_audit.csv`.
- Updated `paper/claim_language_audit.md`.
- Added a claim-registry boundary row for loaded language.
- Added validation and tests for loaded-term counts and boundaries.

## Result

Recorded a bounded language audit of the current manuscript. Loaded terms are either absent or used
only in bounded accounting, unresolved-evidence, or explicitly negated contexts.

## Current Stop Condition

Completion beyond this record requires rerunning the language audit after each manuscript revision
and resolving the underlying evidence blockers before any loaded headline conclusion can be used.
Until those inputs exist, subsidy, loss, underfunding, diversion, artificiality, harm, and
sustainability language remains blocked or bounded under the repository evidence rules.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` after regenerating `MANIFEST.sha256`.
