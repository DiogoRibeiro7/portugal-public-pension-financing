# Quantify bank risk distribution

Instruction file: `prompts/10_bank_transfer_benefit_and_risk_distribution.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.
- Added `data/processed/bank_benefit_risk_distribution.csv`.
- Added validation for channel coverage, duplicate record IDs, unit metadata, 18 bank-level blocked rows, and the blocked net-subsidy classification.
- Added `evidence/bank_benefit_risk_classification_requirements.csv` to tie
  subsidy, net-position, lifecycle and accounting classifications to the
  required bank-level, asset, actuarial, audited-statement and State-financing
  inputs.
- Added validation that fiscal-accounting effects are not treated as bank
  benefits, public-sector lifecycle effects remain diagnostic, and subsidy
  classification cannot be inferred from gross liability transfer.

## Result

Recorded the risk and benefit channels that are supported by registered sources:

- balance-sheet relief from covered bank responsibilities extinguished after transfer;
- liquidity effect from pension-fund assets surrendered to the State, with only a partial aggregate 2011 public-account extract currently populated;
- actuarial-risk transfer for the covered pensions;
- retained bank responsibilities for updates, SAMS contributions, specified survivor/death benefits and complementary benefits;
- fiscal-accounting effects under ESA-95 and ESA-2010;
- demonstrable net subsidy, explicitly blocked rather than inferred.

The 18 participating institutions are present as bank-level net-position rows, but their values remain blank because the registered sources do not provide the final liability present values, surrendered asset values, retained-liability values or sensitivity inputs by bank.

The classification requirements table records the precise missing inputs for
each possible interpretation. It keeps legal channel identification separate
from measured economic benefit and keeps lifecycle public-finance effects
separate from bank-side net positions.

## Current Stop Condition

Completion beyond this record requires bank-level transfer valuation reports, audited pension-fund asset schedules, retained-liability valuations and actuarial sensitivity inputs. Until those inputs exist, the repository must not classify a net subsidy.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
