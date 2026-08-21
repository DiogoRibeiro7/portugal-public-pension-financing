# Build state financing history

Instruction file: `prompts/28_state_guarantee_budget_transfer_and_financing_history.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Reviewed registered State Budget, State account, Social Security, CGA, and
  bank-pension sources available in the repository.
- Added a State-financing rule registry covering budget routes, accounting
  presentation, specific transfers, and transferred-asset financing.
- Added validation that keeps employer contributions, State transfers, special
  transfers, and asset receipts classified separately.
- Preserved the restriction against treating a transfer as underfunding, deficit,
  or legal noncompliance without year-level legal and accounting extraction.

## Result

Recorded a bounded State-financing rule history with executable validation.

## Current Stop Condition

Completion beyond this record requires year-level extraction from State Budget
maps, State accounts, CGA accounts, and Social Security accounts. Until those
inputs exist, annual transfer amounts and residual/fixed/appropriated/settled
formula assignments remain partial.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
