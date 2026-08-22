# Build flow of funds matrix

Instruction file: `prompts/41_cross_entity_flow_of_funds_matrix.md`
Date: 2026-08-19
Updated: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the existing accounting ledgers and validation code.
- Replaced the empty long-form matrix with observed rows from registered CGA, banking-transfer, 2012 banking-cost, debt-financing and BPN sources.
- Marked State Budget to Social Security, CGA to Social Security and public-private asset-transfer rows by whether they disappear under general-government consolidation.
- Kept institutional balances, asset-transfer flows and pension-payment flows in separate `stock_flow` categories.
- Added bridge identifiers and components for the CGA 2011 balance decomposition, 2011 bank asset-transfer values, the 2012 banking cash identity and BPN 2012 rows.
- Added repository validation and tests for schema coverage, duplicate bridge components and core bridge reconciliations.
- Added `evidence/flow_of_funds_bridge_selection_requirements.csv` to require explicit matrix-row selections for combined-balance calculations and keep complete system-wide balances blocked.

## Result

Created `data/processed/pension_flow_of_funds_long.csv` as a checked long-form matrix. The current matrix is still partial because several component ledgers remain unavailable, but available combined-balance and banking-transfer calculations are now tied to explicit selectable rows instead of free-text notes.

## Current Stop Condition

Completion beyond the bounded matrix requires detailed CGA component accounts, RGSS/previdential annual ledgers, FEFSS annual flow data and bank-level transfer schedules. Those quantities remain blocked and are not filled with estimates. Combined-balance calculations must cite explicit selectable rows from `data/processed/pension_flow_of_funds_long.csv` under `evidence/flow_of_funds_bridge_selection_requirements.csv`.

## Validation

This branch ran targeted accounting tests before registry updates. Full quality validation is recorded in the pull request.
