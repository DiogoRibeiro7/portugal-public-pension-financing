# Define bank actuarial bounds

Instruction file: `prompts/38_bank_actuarial_identifiability_bounds.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Replaced the placeholder `evidence/actuarial_identifiability_registry.csv`
  with explicit rows for statutory valuation, discount-rate sensitivity,
  longevity sensitivity, indexation sensitivity, bank-level net positions,
  synthetic microdata and underfunding interpretation.
- Added a bounded present-value envelope helper that only computes ranges when
  explicit lower and upper cash-flow paths and discount-rate grids are supplied.
- Added validation that blocks unsupported point estimates, exact precision
  language, synthetic microdata presented as fact and alternative-rate
  underfunding classifications.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a validated actuarial identifiability gate. Alternative actuarial
valuations remain blocked unless public inputs identify the required cash-flow,
demographic and indexation structures. Discount-rate sensitivity is separated
from longevity and indexation sensitivity, and a higher alternative-rate
liability cannot by itself support an underfunding finding.

## Current Stop Condition

Completion beyond this record requires beneficiary or cohort cash-flow schedules,
age-sex-survivor structure, pension amounts, indexation rules, bank-level asset
composition and retained-obligation values. Until those inputs exist, the
registry permits only source-reported aggregate values and explicitly bounded
sensitivity envelopes.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
