# Build combined balance definitions

Instruction file: `prompts/13_joint_cga_rgss_balance_definitions.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Added `data/processed/joint_balance_definitions.csv` with explicit base, combined, consolidated, historical-adjustment, FEFSS-visible, and bank-special-regime sensitivity perimeters.
- Added `data/processed/joint_balance_definition_rules.csv` with inclusion, exclusion, consolidation, sign-convention, unit, and double-counting guards.
- Added validation for required perimeters, rule coverage, blocked-value handling, and source-limitation metadata.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Recorded competing CGA, RGSS/previdential, combined, consolidated, historically adjusted, FEFSS-visible, and bank-special-regime sensitivity definitions before final values are inspected.

## Current Stop Condition

Completion beyond this record requires the registered annual CGA, previdential, FEFSS, consolidation, historical-adjustment, and bank-special-regime source bridges. Until those inputs exist, the definitions are executable metadata rather than quantitative results.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
