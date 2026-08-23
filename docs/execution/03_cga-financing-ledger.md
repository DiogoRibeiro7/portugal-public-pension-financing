# Build CGA financing ledger

Instruction file: `prompts/03_reconstruct_cga_financing.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Expanded the CGA financing ledger to one row for each year from 1977 through
  2025.
- Preserved the 2011 CGE extract for global balance, PT pension-fund effect,
  balance excluding PT effect, and additional State transfer.
- Added partial 2021, 2022, 2023, and 2024 extractions from official CGA annual reports for
  worker quotations, employer contributions, State Budget transfers, pension
  expenditure, other benefits, subscribers, and retirees.
- Marked years without component extraction as blocked rows rather than leaving
  them absent or treating missing values as zero.
- Added validation for year coverage, source IDs, status labels, missing
  component blockers, and the 2011 balance-decomposition residual.

## Result

Added an executable year-level CGA financing ledger gate and extended it with a
partial 2021, 2022, 2023, and 2024 annual-report extractions.

## Current Stop Condition

Completion beyond this bounded ledger requires additional CGA annual report and
CGE account extraction, especially for other public transfers, investment
income, administration, payroll, and historical years before 2021.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
