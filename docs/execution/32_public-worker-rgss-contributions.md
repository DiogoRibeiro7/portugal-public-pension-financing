# Reconstruct public worker contributions

Instruction file: `prompts/32_reconstruct_public_worker_rgss_contributions_2006_2025.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved existing validated outputs.
- Extended the 2006-2025 public-worker RGSS contribution file with method, pension-basis, uncertainty, aggregate-cap, missing-input and claim-permission fields.
- Added validation that future estimated rows must identify direct observation or reconstruction and cannot exceed aggregate RGSS contribution revenue.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded contribution reconstruction gate. All years remain blank and blocked because administrative public-employer contribution totals, public-worker cohort counts, payroll contribution bases, applicable RGSS rates and aggregate RGSS contribution revenue have not all been extracted from registered sources.

## Current Stop Condition

Completion beyond this gate requires a deterministic extraction chain for direct public-employer RGSS contribution totals or, failing that, public-worker cohort counts, contributory remuneration, applicable worker and employer rates, pension-risk decomposition and aggregate RGSS revenue caps. Until those inputs exist, the repository must not make a quantitative public-worker RGSS contribution claim.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
