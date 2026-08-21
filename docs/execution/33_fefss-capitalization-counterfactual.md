# Reconstruct FEFSS counterfactual

Instruction file: `prompts/33_reconstruct_fefss_return_counterfactual_2006_2025.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved existing validated outputs.
- Expanded the public-worker FEFSS counterfactual companion with actual-asset comparison fields, financing assumptions, retained-resource requirements and claim blockers.
- Added a sensitivity table that separates observed FEFSS returns, a low-risk government-financing benchmark and actual FEFSS asset references.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded capitalization counterfactual gate. The deterministic engine exists, but the counterfactual values remain blank because public-worker contribution cash flows, official FEFSS returns, actual FEFSS asset stocks and low-risk benchmark rates are not yet fully reconstructed.

## Current Stop Condition

Completion beyond this gate requires source-backed cash flows, return measures, actual FEFSS assets and benchmark rates. Any future result must state that the hypothetical reserve requires additional retained resources unless an offsetting financing assumption is specified.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
