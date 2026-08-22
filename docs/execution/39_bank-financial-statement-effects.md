# Measure bank statement effects

Instruction file: `prompts/39_bank_financial_statement_liability_relief.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Replaced the empty `data/processed/bank_financial_statement_effects.csv`
  placeholder with 2011-2012 institution-year coverage for the 18 DL127
  participating institutions.
- Added `evidence/bank_financial_statement_source_evidence.csv` to record the
  audited-statement documents and extraction fields required for each
  institution before bank-side relief can be measured.
- Added validation that blocks measured values until audited statement extracts
  exist and requires any material-benefit claim to identify a measurable net
  channel rather than gross liability extinguishment alone.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a validated audited-statement extraction gate. The repository now has a
complete institution coverage frame, but liability derecognition, assets
surrendered, P&L gain or loss, capital effect, retained obligations and net
benefit values remain blank until primary financial statements are acquired and
extracted.

## Current Stop Condition

Completion beyond this record requires 2011 and 2012 audited annual reports or
branch financial statements for each participating institution, page-level
extraction evidence for pension liability derecognition, assets surrendered,
P&L effects, capital effects and retained obligations, and reconciliation to the
aggregate State transaction. Until those inputs exist, the repository must not
claim a material bank benefit.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
