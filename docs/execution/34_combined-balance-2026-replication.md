# Replicate 2026 combined balance

Instruction file: `prompts/34_replicate_2026_combined_balance_and_2025_deficit.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Replaced the header-only combined-balance replication table with a blocked annual series scaffold for 2006-2025 and explicit 2025 definition rows.
- Added `data/processed/combined_balance_component_bridge_2026.csv` to separate base components, adjustments, reclassifications, alternative FEFSS treatment, and bank-special-regime sensitivity.
- Added validation for required definitions, bridge components, sign-effect labels, blocked-value handling, and the manuscript definition-versus-endorsement boundary.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded replication gate for the combined-balance and 2025 adjusted-deficit claims. The annual series and alternative perimeter rows are present, but values remain blank until the working-group report package and official component bridges are registered.

## Current Stop Condition

Completion beyond this record requires the registered working-group formula, institutional perimeter, annual component source tables, adjustment bridge, and bank-special-regime sensitivity inputs. Until those inputs exist, sign and magnitude classifications remain blocked.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
