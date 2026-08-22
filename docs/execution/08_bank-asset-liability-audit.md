# Audit bank assets and liabilities

Instruction file: `prompts/08_bank_transfer_asset_liability_audit.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Added `data/processed/bank_asset_liability_institution_requirements.csv` to enumerate the 18 participating institutions and the bank-level liability, asset-composition, final-adjustment and cash-flow schedules required for the audit.
- Added validation that the institution requirements match the DL127 asset-trace panel and preserve the rule that alternative discount-rate results are sensitivity outputs, not standalone underfunding findings.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded institution-level requirements gate. The repository still records only aggregate CGE extracts and legal parameters; bank-level statutory equality and sensitivity surfaces remain blocked until final valuation and asset-composition schedules are acquired.

## Current Stop Condition

Completion beyond this record requires bank-level final actuarial liability values, transferred-asset composition, independent valuation outputs, cash-flow schedules and defensible mortality/longevity assumptions. Until those inputs exist, the operation must not be classified as underfunded from sensitivity assumptions alone.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
