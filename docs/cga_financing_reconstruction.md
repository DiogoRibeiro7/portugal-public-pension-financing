# CGA financing ledger

Status: `partial_cge_extract`

This note documents `data/processed/cga_financing_ledger.csv`.

## Current Extract

The current ledger contains a bounded 2011 extract from `DGO_CGE_2011`.

Extracted CGE 2011 values:

- CGA global balance: EUR 186.2 million.
- PT pension-fund effect in CGA: EUR 476.7 million.
- CGA global balance excluding the PT pension-fund effect: EUR -290.6 million.
- Additional State Budget transfer to compensate CGA own-revenue loss: EUR 172.6 million.

The balance decomposition reconciles with a EUR 0.1 million rounding residual:

`186.2 = 476.7 + (-290.6) + 0.1`

## Limitation

CGE 2011 volume 1 does not provide a full CGA component ledger separating employee quotations, employer contributions, total State Budget transfers, other public transfers, investment income, pension expenditure, other benefits, administration, contributor count, pensioner count and payroll. Those missing components are recorded in `evidence/data_quality_registry.csv`.

Rows marked `partial_cge_extract` must not be used as a complete financing identity. `python -m portugal_pensions.cli validate-evidence` enforces this distinction.
