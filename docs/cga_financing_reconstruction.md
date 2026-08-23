# CGA financing ledger

Status: `partial_bounded_reconstruction`

This note documents `data/processed/cga_financing_ledger.csv`.

## Ledger Scope

The ledger now contains one row for every study year from 1977 through 2025.
Rows without extracted component values are explicit blockers, not zeros. They
point to registered official account routes and carry the missing component list
needed before a complete financing identity can be computed.

## Current Extracts

The ledger currently contains two partial quantitative extracts: the bounded
2011 row from `DGO_CGE_2011` and a 2024 CGA annual-report extract from
`CGA_REPORT_2024`.

Extracted CGE 2011 values:

- CGA global balance: EUR 186.2 million.
- PT pension-fund effect in CGA: EUR 476.7 million.
- CGA global balance excluding the PT pension-fund effect: EUR -290.6 million.
- Additional State Budget transfer to compensate CGA own-revenue loss: EUR 172.6 million.

The balance decomposition reconciles with a EUR 0.1 million rounding residual:

`186.2 = 476.7 + (-290.6) + 0.1`

Extracted CGA 2024 values from the annual report:

- Worker quotations: EUR 1,364.79288482 million.
- Employer contributions: EUR 2,904.15942995 million.
- State Budget transfers: EUR 7,126.116564 million.
- Pension expenditure: EUR 12,329.25635274 million.
- Other benefits: EUR 19.20822306 million.
- Subscribers: 359,795.
- Retirees: 494,354.

The 2024 pensioner-count field records aposentados/reformados only. Survival
and other pensionists are visible in the report but are not loaded into that
single ledger field.

## Limitations

CGE 2011 volume 1 does not provide a full CGA component ledger separating all
required financing, expenditure, population, and payroll components. The 2024
CGA report extract resolves several high-value components but still leaves
other public transfers, investment income, administration, and contribution-base
payroll unresolved.

Rows marked `partial_cge_extract`, `partial_cga_report_extract`, or
`blocked_missing_primary_account_components` must not be used as complete
financing identities. `python -m portugal_pensions.cli validate-evidence`
enforces this distinction, the 1977-2025 row coverage, source IDs, and the 2011
balance-decomposition residual.
