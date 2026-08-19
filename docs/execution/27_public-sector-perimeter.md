# Map public sector perimeter

Instruction file: `prompts/27_public_sector_perimeter_and_employer_class_mapping.md`
Date: 2026-08-19
Status: `blocked_by_source_work`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Recorded employer-class mapping prerequisites.

## Current Stop Condition

Completion beyond this record requires the registered primary sources and deterministic extraction chain needed by the task. Until those inputs exist, any quantitative result remains blocked or partial under the repository evidence rules.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` after regenerating `MANIFEST.sha256`.
