# CGA financing ledger

Status: `partial_bounded_reconstruction`

This note documents `data/processed/cga_financing_ledger.csv`.

## Ledger Scope

The ledger now contains one row for every study year from 1977 through 2025.
Rows without extracted component values are explicit blockers, not zeros. They
point to registered official account routes and carry the missing component list
needed before a complete financing identity can be computed.

## Current Extracts

The ledger currently contains eleven partial quantitative extracts: the bounded
2011 row from `DGO_CGE_2011` and 2015-2024 CGA annual-report extracts from
`CGA_REPORT_2015`, `CGA_REPORT_2016`, `CGA_REPORT_2017`, `CGA_REPORT_2018`,
`CGA_REPORT_2019`, `CGA_REPORT_2020`, `CGA_REPORT_2021`, `CGA_REPORT_2022`,
`CGA_REPORT_2023`, and `CGA_REPORT_2024`.

Extracted CGE 2011 values:

- CGA global balance: EUR 186.2 million.
- PT pension-fund effect in CGA: EUR 476.7 million.
- CGA global balance excluding the PT pension-fund effect: EUR -290.6 million.
- Additional State Budget transfer to compensate CGA own-revenue loss: EUR 172.6 million.

The balance decomposition reconciles with a EUR 0.1 million rounding residual:

`186.2 = 476.7 + (-290.6) + 0.1`

Extracted CGA annual-report values:

- 2015 worker quotations: EUR 1,251.20368594 million.
- 2015 employer contributions: EUR 2,594.29398748 million.
- 2015 State Budget transfers: EUR 4,858.330040 million.
- 2015 pension expenditure: EUR 9,643.30077242 million.
- 2015 other benefits: EUR 17.28967514 million.
- 2015 subscribers: 473,446.
- 2015 retirees: 486,269.
- 2016 worker quotations: EUR 1,279.87792524 million.
- 2016 employer contributions: EUR 2,665.81717950 million.
- 2016 State Budget transfers: EUR 4,926.016419 million.
- 2016 pension expenditure: EUR 9,652.88102861 million.
- 2016 other benefits: EUR 16.84754487 million.
- 2016 subscribers: 463,861.
- 2016 retirees: 482,614.
- 2017 worker quotations: EUR 1,254.81417605 million.
- 2017 employer contributions: EUR 2,616.83657937 million.
- 2017 State Budget transfers: EUR 4,993.4273 million.
- 2017 pension expenditure: EUR 9,669.01867476 million.
- 2017 other benefits: EUR 17.50028394 million.
- 2017 subscribers: 453,977.
- 2017 retirees: 481,877.
- 2018 worker quotations: EUR 1,255.68891818 million.
- 2018 employer contributions: EUR 2,648.46821170 million.
- 2018 State Budget transfers: EUR 5,224.6925 million.
- 2018 pension expenditure: EUR 9,838.34806805 million.
- 2018 other benefits: EUR 19.14346397 million.
- 2018 subscribers: 443,528.
- 2018 retirees: 479,132.
- 2019 worker quotations: EUR 1,247.65131329 million.
- 2019 employer contributions: EUR 2,632.88601538 million.
- 2019 State Budget transfers: EUR 5,262.518512 million.
- 2019 pension expenditure: EUR 9,888.31348072 million.
- 2019 other benefits: EUR 19.88961162 million.
- 2019 subscribers: 431,132.
- 2019 retirees: 481,014.
- 2020 worker quotations: EUR 1,274.62763604 million.
- 2020 employer contributions: EUR 2,707.57963028 million.
- 2020 State Budget transfers: EUR 5,410.083453 million.
- 2020 pension expenditure: EUR 10,131.42361827 million.
- 2020 other benefits: EUR 21.49160065 million.
- 2020 subscribers: 416,874.
- 2020 retirees: 482,429.
- 2021 worker quotations: EUR 1,286.29548744 million.
- 2021 employer contributions: EUR 2,718.53039275 million.
- 2021 State Budget transfers: EUR 5,488.799101 million.
- 2021 pension expenditure: EUR 10,225.78228324 million.
- 2021 other benefits: EUR 19.10787935 million.
- 2021 subscribers: 402,099.
- 2021 retirees: 481,942.
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

The 2015, 2016, 2017, 2018, and 2019 reports label worker quotations as `Quotas` and employer
contributions as `Contribuição de Entidades`; these are loaded into the
comparable ledger fields while retaining the source labels in the extraction
audit.

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
