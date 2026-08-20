# Replicate ESA treatment

Instruction file: `prompts/11_replicate_esa95_esa2010_treatment.md`
Date: 2026-08-19
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Extracted the European Commission ex-post evaluation text to an interim file for line-level audit.
- Added `data/processed/bank_esa_treatment_bridge.csv` to record the ESA-95 treatment, ESA-2010 treatment, and remaining bridge gap.
- Added a validation contract for the bridge dataset, including the percent-of-GDP identity for rows that contain both euro and GDP-denominator values.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

The ESA-95 result is partially replicated by reconciling the CGE 2011 amount of EUR 5993.2m to the published 3.5 percent of GDP treatment, implying a GDP denominator of EUR 171234.285714m. The European Commission source confirms the accounting discontinuity: ESA-95 treated the transfer as revenue-increasing with a direct deficit effect, while ESA-2010 treated the same operation as a financial transaction with no direct deficit effect.

## Current Stop Condition

Full independent restatement remains blocked until official machine-readable ESA-95 and ESA-2010 national-accounts or EDP bridge tables are acquired. The repository therefore records this as a bounded reconstruction rather than a completed national-accounts reproduction.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
