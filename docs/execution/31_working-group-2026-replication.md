# Replicate 2026 working group

Instruction file: `prompts/31_replicate_2026_working_group_report.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Registered the five required 2026 working-group claim targets in `evidence/public_claim_registry.csv`.
- Added a companion blocked-replication table at `data/processed/working_group_2026_replication.csv`.
- Added validation checks that require the target claims and prevent copied or replicated values while the primary report package is missing.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded claim gate for the working-group replication. The repository now
tracks the required targets, the missing artifacts, and the reason no numerical
replication can yet be classified.

## Current Stop Condition

Completion beyond this record requires the registered primary report, annexes,
methodological notes, released spreadsheets, and source-table bridges needed by
the task. Until those inputs exist, each target remains
`blocked_primary_source_missing` under the repository evidence rules.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
