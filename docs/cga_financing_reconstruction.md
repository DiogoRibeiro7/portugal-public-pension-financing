# CGA financing ledger

Status: `partial_bounded_reconstruction`

This note documents `data/processed/cga_financing_ledger.csv`.

## Ledger Scope

The ledger now contains one row for every study year from 1977 through 2025.
Rows without extracted component values are explicit blockers, not zeros. They
point to registered official account routes and carry the missing component list
needed before a complete financing identity can be computed.

## Current Extracts

The ledger currently contains four partial quantitative extracts: the bounded
2011 row from `DGO_CGE_2011` and 2022-2024 CGA annual-report extracts from
`CGA_REPORT_2022`, `CGA_REPORT_2023`, and `CGA_REPORT_2024`.

Extracted CGE 2011 values:

- CGA global balance: EUR 186.2 million.
- PT pension-fund effect in CGA: EUR 476.7 million.
- CGA global balance excluding the PT pension-fund effect: EUR -290.6 million.
- Additional State Budget transfer to compensate CGA own-revenue loss: EUR 172.6 million.

The balance decomposition reconciles with a EUR 0.1 million rounding residual:

`186.2 = 476.7 + (-290.6) + 0.1`

Extracted CGA annual-report values:

- 2022 worker quotations: EUR 1,246.05687117 million.
- 2022 employer contributions: EUR 2,646.09273500 million.
- 2022 State Budget transfers: EUR 5,827.82 million.
- 2022 pension expenditure: EUR 10,752.22497888 million.
- 2022 other benefits: EUR 17.08731683 million.
- 2022 subscribers: 386,216.
- 2022 retirees: 482,938.
- 2023 worker quotations: EUR 1,278.52621286 million.
- 2023 employer contributions: EUR 2,719.38860724 million.
- 2023 State Budget transfers: EUR 6,208.0845 million.
- 2023 pension expenditure: EUR 11,242.25151920 million.
- 2023 other benefits: EUR 20.28792585 million.
- 2023 subscribers: 380,060.
- 2023 retirees: 487,576.
- 2024 worker quotations: EUR 1,364.79288482 million.
- 2024 employer contributions: EUR 2,904.15942995 million.
- 2024 State Budget transfers: EUR 7,126.116564 million.
- 2024 pension expenditure: EUR 12,329.25635274 million.
- 2024 other benefits: EUR 19.20822306 million.
- 2024 subscribers: 359,795.
- 2024 retirees: 494,354.

The pensioner-count field records aposentados/reformados only. Survival and
other pensionists are visible in the reports but are not loaded into that single
ledger field.

## Limitations

CGE 2011 volume 1 does not provide a full CGA component ledger separating all
required financing, expenditure, population, and payroll components. The
annual-report extracts resolve several high-value components but still leave
other public transfers, investment income, administration, and contribution-base
payroll unresolved.

Rows marked `partial_cge_extract`, `partial_cga_report_extract`, or
`blocked_missing_primary_account_components` must not be used as complete
financing identities. `python -m portugal_pensions.cli validate-evidence`
enforces this distinction, the 1977-2025 row coverage, source IDs, and the 2011
balance-decomposition residual.
