# Build counterfactual regimes

Instruction file: `prompts/14_counterfactual_financing.md`
Date: 2026-08-19
Updated: 2026-08-20
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the preregistered counterfactual registry and current processed ledgers.
- Added `data/processed/counterfactual_financing_regimes.csv` to bind each registered scenario to a stock-flow treatment, financing adjustment rule, required input dataset and implemented helper where available.
- Preserved the distinction between cash-flow substitutions, additional reserve expenditure, stock valuation sensitivity and bank-transfer lifecycle analysis.
- Added validation that each registered scenario is represented, duplicate scenario components are rejected and funded-reserve rows explicitly treat contributions as additional expenditure unless an offset is named.
- Added tests for repository validity, scenario coverage and funded-reserve stock-flow treatment.

## Result

Implemented the preregistered counterfactual regimes as a checked rule table. Quantitative scenario outputs remain blocked where the required payroll, contribution, return, bank cash-flow or asset-income data are not yet registered.

## Current Stop Condition

Completion beyond this bounded rule implementation requires CGA component ledgers, public-worker RGSS contribution paths, FEFSS return series and full bank pension cash-flow schedules. Missing inputs are recorded as gaps rather than substituted with estimates.

## Validation

This branch ran targeted counterfactual tests before registry updates. Full quality validation is recorded in the pull request.
