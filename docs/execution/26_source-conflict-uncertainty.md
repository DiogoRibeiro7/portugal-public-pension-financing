# Add conflict policy

Instruction file: `prompts/26_source_conflict_revisions_and_uncertainty.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Added bounded rows to `evidence/source_conflict_registry.csv` for observed bank-transfer and special-regime source differences.
- Added linked uncertainty rows to `evidence/uncertainty_registry.csv`, including an unresolved 2011 range where the current evidence does not identify a single financing basis.
- Replaced the placeholder policy with explicit difference classes, preference rules, tolerances, and range-propagation requirements.
- Added a validation gate and tests for source, concept, unit, status, numeric bound, and unresolved-central-value checks.
- Preserved existing validated outputs and did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added an executable conflict and uncertainty gate. The current result is a bounded reconstruction: reconciled rows are documented where source differences are rounding, approximation, or estimand-specific ESA treatment; unresolved rows remain bounded ranges that must be propagated downstream.

## Current Stop Condition

Completion beyond this record requires a complete source-pair inventory across the historical horizon and the missing bank-level transfer schedules, revision tables, and transaction-level national-accounts bridges. Until those inputs exist, unresolved ranges cannot be collapsed into point estimates under the repository evidence rules.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
