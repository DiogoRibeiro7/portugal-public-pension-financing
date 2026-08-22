# Quantify bank debt effects

Instruction file: `prompts/42_bank_transfer_debt_and_financing_cost.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Acquired the Banco de Portugal 2012 annual report and extracted observed public borrowing-cost anchors.
- Replaced the placeholder debt file with `data/processed/bank_transfer_debt_financing_effects.csv`.
- Added financing-cost sensitivities for the 2011 recorded asset receipt using 2.6 percent, 3.7 percent, and 7.3 percent observed-rate anchors.
- Kept gross-debt classification and full lifecycle cost blocked because final cash, public-debt-security, other-asset composition, disposal path, and pension cash-flow ledgers are not registered.
- Added `evidence/bank_debt_financing_classification_requirements.csv` to gate gross-debt treatment, government-bond double-counting, lifecycle net-effect classification, and claim language.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

The ledger records three distinct facts. First, CGE 2011 reports EUR 3263.1m as the 2011 asset-title receipt and EUR 5993.2m as the aggregate transfer value. Second, Tribunal de Contas reports EUR 516.0m in 2012 banking substitute-regime pension payments with matching rounded current-transfer financing. Third, using Banco de Portugal 2012 observed-rate anchors, the potential annual interest saving on the EUR 3263.1m receipt ranges from EUR 84.8406m at the 2.6 percent programme-loan rate to EUR 238.2063m at the 7.3 percent December 2012 10-year Treasury yield.

## Current Stop Condition

The result cannot classify the operation as beneficial or harmful to consolidated public finances. That requires the final asset composition, gross-debt stock treatment, government-bond consolidation bridge, asset disposal path, and full pension cash-flow or liability-cost path. These gaps are recorded in `evidence/data_quality_registry.csv` and enforced by `evidence/bank_debt_financing_classification_requirements.csv`.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
