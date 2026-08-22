# Replicate bank pension cost

Instruction file: `prompts/12_replicate_2012_bank_pension_cost.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Acquired the Tribunal de Contas 2013 Social Security budget-execution report for January-December 2012 and converted it to text for line-level extraction.
- Added `data/processed/bank_pension_cost_2012.csv` to reconcile the European Commission rounded benchmark to the official-account amount.
- Updated the annual special-regime ledger for 2012 from the rounded EC placeholder to the official EUR 516.0m financing and pension-payment execution.
- Added validation for the official amount, benchmark residual, units, year, perimeter metadata, and financing residual identity.
- Added `evidence/bank_pension_cost_2012_component_requirements.csv` to gate component splits, lifecycle extensions, and manuscript language around the 2012 amount.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

The European Commission statement that the transfer generated about EUR 0.5bn of additional pension expenditure in 2012 is now reconciled to an official account extraction. The Tribunal de Contas report, using IGFSS and Declaração n.º 58/2013 data, reports EUR 516.0m in 2012 payments for the banking substitute-regime pensions and the same rounded amount in current-transfer financing.

The official report also identifies EUR 515.8m from the State Budget and EUR 0.1359m from CGA for the BPN-related component, which rounds to the EUR 516.0m total. Administrative personnel and goods/services allocations for this regime show zero execution in the cited annex notes.

## Current Stop Condition

The result remains bounded because the registered evidence does not split the EUR 516.0m by bank-level pension populations, monthly cash flows, retained-liability components, or post-2012 asset and financing lifecycle paths. Those gaps are recorded in `evidence/data_quality_registry.csv` and enforced by `evidence/bank_pension_cost_2012_component_requirements.csv`.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
