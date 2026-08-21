# Quantify post-2006 reallocation

Instruction file: `prompts/06_post_2006_public_worker_reallocation.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved existing validated outputs.
- Added a processed bridge that separates the mechanical post-2006 RGSS contribution-flow channel from demographic change, wage growth and general labour-market effects.
- Added a deterministic flow identity for future completed rows and validation that blocks quantitative claims while cohort, payroll and rate inputs are missing.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded public-worker reallocation bridge with year coverage from 2006 through 2025. The bridge records the legal mechanism and the accounting identity needed to compute the mechanical flow once source inputs are available, but leaves contribution amounts blank because the required public-worker cohort counts, contribution bases and applicable RGSS rates are not yet fully reconstructed.

## Current Stop Condition

Completion beyond this bounded bridge requires a deterministic extraction chain for public-worker new-entrant counts, payroll contribution bases and applicable RGSS worker and employer rates. Until those inputs exist, the repository must not make a quantitative post-2006 reallocation claim.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
