# Quantify bank risk distribution

Instruction file: `prompts/10_bank_transfer_benefit_and_risk_distribution.md`
Date: 2026-08-19
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.
- Added `data/processed/bank_benefit_risk_distribution.csv`.
- Added validation for channel coverage, duplicate record IDs, unit metadata, 18 bank-level blocked rows, and the blocked net-subsidy classification.

## Result

Recorded the risk and benefit channels that are supported by registered sources:

- balance-sheet relief from covered bank responsibilities extinguished after transfer;
- liquidity effect from pension-fund assets surrendered to the State, with only a partial aggregate 2011 public-account extract currently populated;
- actuarial-risk transfer for the covered pensions;
- retained bank responsibilities for updates, SAMS contributions, specified survivor/death benefits and complementary benefits;
- fiscal-accounting effects under ESA-95 and ESA-2010;
- demonstrable net subsidy, explicitly blocked rather than inferred.

The 18 participating institutions are present as bank-level net-position rows, but their values remain blank because the registered sources do not provide the final liability present values, surrendered asset values, retained-liability values or sensitivity inputs by bank.

## Current Stop Condition

Completion beyond this record requires bank-level transfer valuation reports, audited pension-fund asset schedules, retained-liability valuations and actuarial sensitivity inputs. Until those inputs exist, the repository must not classify a net subsidy.

## Validation

`python -m portugal_pensions.cli validate-evidence` validates the processed ledger and the unresolved classification boundaries.
