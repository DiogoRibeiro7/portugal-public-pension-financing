# Reconcile bank state financing

Instruction file: `prompts/09_bank_transfer_long_run_state_financing.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.
- Added a typed validation path for the annual bank special-regime ledger.
- Registered the legal State-financing rule separately from annual executed values.
- Added an explicit 2012-2025 annual ledger with missing components left blank rather than treated as zero.
- Added `evidence/bank_state_financing_reconciliation_requirements.csv` to record
  the exact annual components and primary records needed before residuals can be
  computed or classified.
- Added validation that `evidence/bank_special_regime_annual.csv` and
  `data/processed/bank_transfer_long_run.csv` remain identical, and that the
  residual is treated as a diagnostic rather than a Social Security loss while
  required components are missing.

## Result

`evidence/bank_special_regime_annual.csv` and `data/processed/bank_transfer_long_run.csv` now cover 2012-2025.

The ledger records the published European Commission benchmark that transferred bank pensions added roughly EUR 0.5 billion of pension expenditure in 2012. That benchmark remains `to_replicate` through official Social Security accounts.

The 2012 row is now the only annual row with official transfer, expenditure and
administrative-cost values populated. Rows after 2012 remain blocked, and the
requirements table records why each missing component cannot be silently set to
zero.

For the annual State-financing residual, the current result is blocked. The registered sources establish the legal rule that the State finances the transferred pensions through a specific transfer to Social Security, but they do not yet provide the full annual component set needed to compute and classify residuals:

- specific State transfer;
- pension expenditure;
- administrative costs;
- attributable investment income or asset drawdown;
- other financing;
- timing adjustments.

It also requires ownership or management records before attributing transferred
asset income or drawdown to Social Security.

## Current Stop Condition

Completion beyond this record requires annual Conta da Seguranca Social or DGO execution tables that expose the special banking regime transfer and cost components. Until those inputs exist, missing components must not be interpreted as zero and the residual must not be classified as a Social Security loss.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
