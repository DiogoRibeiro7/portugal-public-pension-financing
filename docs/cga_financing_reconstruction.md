# CGA financing ledger

Status: `partial_bounded_reconstruction`

This note documents `data/processed/cga_financing_ledger.csv`.

## Ledger Scope

The ledger now contains one row for every study year from 1977 through 2025.
Rows without extracted component values are explicit blockers, not zeros. They
point to registered official account routes and carry the missing component list
needed before a complete financing identity can be computed.

## Current Extract

The only current quantitative CGA financing extract remains the bounded 2011 row
from `DGO_CGE_2011`.

Extracted CGE 2011 values:

- CGA global balance: EUR 186.2 million.
- PT pension-fund effect in CGA: EUR 476.7 million.
- CGA global balance excluding the PT pension-fund effect: EUR -290.6 million.
- Additional State Budget transfer to compensate CGA own-revenue loss: EUR 172.6 million.

The balance decomposition reconciles with a EUR 0.1 million rounding residual:

`186.2 = 476.7 + (-290.6) + 0.1`

## Limitations

CGE 2011 volume 1 does not provide a full CGA component ledger separating
employee quotations, employer contributions, total State Budget transfers, other
public transfers, investment income, pension expenditure, other benefits,
administration, contributor count, pensioner count and payroll. Those missing
components are recorded both in the ledger row and in
`evidence/data_quality_registry.csv`.

Rows marked `partial_cge_extract` or `blocked_missing_primary_account_components`
must not be used as complete financing identities. `python -m
portugal_pensions.cli validate-evidence` enforces this distinction, the
1977-2025 row coverage, source IDs, and the 2011 balance-decomposition residual.
