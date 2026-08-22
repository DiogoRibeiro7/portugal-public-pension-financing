# Bank Asset Trace Methodology

Status: `partial_bounded_reconstruction`

This note documents:

- `data/processed/bank_asset_liability_audit.csv`
- `data/processed/bank_asset_liability_sensitivity.csv`
- `data/processed/bank_asset_trace.csv`
- `data/processed/bank_asset_trace_controls.csv`

## Current Extract

CGE 2011 provides two aggregate public-account values:

- EUR 5,993.2 million for the banking pension-fund transfer, reported as 3.5 percent of GDP.
- EUR 3,263.1 million recorded in 2011 as part of the transfer to the State of asset ownership from credit-institution pension funds.

These values do not constitute a final bank-level statutory equality test. They are different accounting views of the operation and must not be reconciled as if they were the same ledger item.

## Asset-Tracing Controls

`data/processed/bank_asset_trace_controls.csv` is the machine-readable control
layer for the asset trace. It separates seven questions:

- the observed 2011 State receipt;
- cash transferred;
- Portuguese public-debt securities transferred;
- other assets transferred;
- whether assets were held by Social Security or FEFSS;
- the post-transfer disposal, retention, consolidation or reclassification path;
- bank-level asset composition across the 18 DL127 institutions.

The current evidence supports only the aggregate 2011 State receipt. Cash,
public-debt securities, other assets, bank-level composition and post-transfer
lifecycle treatment remain blocked until primary Treasury, debt-management,
valuation or transfer-schedule records are acquired.

## Ownership Rule

The asset trace treats the registered transfer as a State asset receipt. It does
not assume a ring-fenced Social Security or FEFSS fund. Long-run burden
calculations may use the EUR 3,263.1 million value as a State financing-resource
row, but they may not credit Social Security with investment income, drawdown or
asset returns unless an ownership or management record supports that treatment.

## Missing Inputs

The registered sources do not yet provide, for every participating institution:

- final actuarial liability transferred;
- final value of assets delivered;
- cash, Portuguese public debt and other-asset composition;
- final adjustment amounts;
- pension cash-flow schedules and demographic inputs for sensitivity analysis.
- Treasury cash receipt records;
- public-debt-security schedules and gross-debt treatment;
- other-asset disposal or retention records;
- Social Security or FEFSS ownership and management records, if any.

## Sensitivity Rule

The repository records the required 2 percent to 6 percent discount-rate grid, but liability values are blank until cash-flow and mortality/longevity inputs are acquired. A higher liability under a lower discount rate is an economic sensitivity, not by itself proof that the 2011 statutory transfer was legally underfunded.

`python -m portugal_pensions.cli validate-evidence` validates the aggregate
extracts, 18 blocked bank-level asset rows, the asset-tracing controls and the
complete 2 percent to 6 percent sensitivity grid.
