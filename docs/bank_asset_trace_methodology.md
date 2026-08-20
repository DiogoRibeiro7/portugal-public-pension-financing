# Bank asset-liability audit

Status: `partial_aggregate_extract`

This note documents:

- `data/processed/bank_asset_liability_audit.csv`
- `data/processed/bank_asset_liability_sensitivity.csv`
- `data/processed/bank_asset_trace.csv`

## Current Extract

CGE 2011 provides two aggregate public-account values:

- EUR 5,993.2 million for the banking pension-fund transfer, reported as 3.5 percent of GDP.
- EUR 3,263.1 million recorded in 2011 as part of the transfer to the State of asset ownership from credit-institution pension funds.

These values do not constitute a final bank-level statutory equality test. They are different accounting views of the operation and must not be reconciled as if they were the same ledger item.

## Missing Inputs

The registered sources do not yet provide, for every participating institution:

- final actuarial liability transferred;
- final value of assets delivered;
- cash, Portuguese public debt and other-asset composition;
- final adjustment amounts;
- pension cash-flow schedules and demographic inputs for sensitivity analysis.

## Sensitivity Rule

The repository records the required 2 percent to 6 percent discount-rate grid, but liability values are blank until cash-flow and mortality/longevity inputs are acquired. A higher liability under a lower discount rate is an economic sensitivity, not by itself proof that the 2011 statutory transfer was legally underfunded.

`python -m portugal_pensions.cli validate-evidence` validates the aggregate extracts, 18 blocked bank-level asset rows, and the complete 2 percent to 6 percent sensitivity grid.
