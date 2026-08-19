# Add conflict policy

Instruction file: `prompts/26_source_conflict_revisions_and_uncertainty.md`
Date: 2026-08-19
Status: `partial`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Documented conflict classes and uncertainty handling.

## Current Stop Condition

Completion beyond this record requires the registered primary sources and deterministic extraction chain needed by the task. Until those inputs exist, any quantitative result remains blocked or partial under the repository evidence rules.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` after regenerating `MANIFEST.sha256`.
