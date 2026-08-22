# Reconstruct bank worker flows

Instruction file: `prompts/36_bank_worker_integration_contributions_2009_2011.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Replaced the header-only bank-worker RGSS contribution table with bounded rows for 2009 new-worker entry, 2011 active-worker CAFEB integration, and the excluded DL127 pensioner population.
- Added `data/processed/bank_worker_legal_population_mapping.csv` to separate active-worker contribution populations from pensioners already in payment.
- Added validation for required populations, blank blocked values, source/status metadata, and the rule that active-worker inflows are not pension-fund assets.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded flow-separation gate for bank-worker RGSS contributions. The legal populations are identified, but contribution values remain blocked until official population, contribution, Social Security account, and programme-evaluation reconciliation tables are registered.

## Current Stop Condition

Completion beyond this record requires official bank-worker population counts, contribution totals, CAFEB reconciliation tables, and Social Security account/programme-evaluation benchmarks. Until those inputs exist, active-worker contribution inflows remain unquantified and must not be treated as transferred pension-fund assets.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
