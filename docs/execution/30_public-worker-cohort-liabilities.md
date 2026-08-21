# Model public worker cohorts

Instruction file: `prompts/30_post_2006_public_worker_cohort_and_future_liabilities.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved existing validated outputs.
- Added `evidence/public_worker_liability_assumptions.csv` as the explicit gate linking current RGSS contribution flows to accrued future pension rights.
- Added validation that blocks any free-sustainability interpretation unless the rights caveat and required actuarial inputs are preserved.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded public-worker future-rights assumption gate. No actuarial value is estimated because cohort counts, service histories, contribution bases, benefit formula inputs, mortality assumptions, indexation rules and discount-rate assumptions are not yet reconstructed.

## Current Stop Condition

Completion beyond this gate requires a deterministic extraction chain for the public-worker cohorts and a defensible aggregate or microdata-based pension-rights valuation framework. Until those inputs exist, the repository must report current-flow effects separately from intertemporal pension-rights effects.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
