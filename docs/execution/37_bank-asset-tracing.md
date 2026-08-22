# Trace bank assets

Instruction file: `prompts/37_trace_2011_transferred_bank_assets.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Added `data/processed/bank_asset_trace_controls.csv` to separate the observed
  2011 State receipt from cash, Portuguese public-debt securities, other assets,
  Social Security or FEFSS ownership, post-transfer lifecycle treatment and
  bank-level composition.
- Updated `docs/bank_asset_trace_methodology.md` with the ownership rule: the
  observed asset receipt may be used as a State financing-resource row, but not
  as Social Security investment income or a ring-fenced FEFSS asset without
  ownership or management records.
- Added validation that preserves the EUR 3,263.1 million observed receipt,
  blocks unsupported ring-fence assumptions and requires primary records before
  asset composition or lifecycle treatment is used.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a validated bank asset-tracing control gate. The repository now records
what is observed, what remains missing, and how long-run burden calculations may
use the 2011 asset receipt without assuming the assets formed a Social Security
or FEFSS reserve.

## Current Stop Condition

Completion beyond this record requires final bank-level asset schedules, Treasury
cash receipt records, public-debt-security schedules, other-asset disposal
records, gross-debt treatment and any Social Security or FEFSS ownership or
management records. Until those inputs exist, asset composition and lifecycle
effects remain blocked.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
