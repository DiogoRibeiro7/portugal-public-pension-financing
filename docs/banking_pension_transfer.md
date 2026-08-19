# Banking-sector pension transfer: research note

## Why it belongs in this paper

The transfer of banking-sector pension responsibilities changes the interpretation of Social Security balances because it introduces a large, discrete transfer of privately managed pension assets together with long-lived pension obligations.

It is analytically distinct from the CGA problem but belongs in the same paper because both cases demonstrate why current cash balances cannot be interpreted without reconstructing the historical financing perimeter.

## Legal facts to reproduce from primary sources

Decree-Law 127/2011 provides that:

- Social Security assumes specified pensions in payment on 31 December 2011.
- The State receives ownership of the corresponding portion of pension-fund assets.
- The State is responsible for financing those pensions, including administrative costs, through a specific transfer to Social Security.
- The asset value is intended to equal the actuarial value of the responsibilities transferred.
- The statutory valuation uses a 4% discount rate and specified mortality tables.
- Up to 50% of transferred assets could consist of Portuguese public debt securities valued at market prices.
- At least 55% of the provisional liability value was to be transferred by 31 December 2011, with the remainder following in 2012.
- Once the relevant transfer was completed, the covered bank responsibilities became definitively and irreversibly extinguished.
- Banks retained responsibility for specified pension updates, SAMS contributions, certain survivor benefits and complementary benefits.

These are legal-design facts, not findings on whether the operation was economically fair.

## Registry status

`evidence/bank_pension_transfer_registry.csv` now records the primary-source legal timeline for Decree-Law 54/2009, Decree-Law 1-A/2011, Decree-Law 127/2011 and Decree-Law 88/2012. For Decree-Law 127/2011 it records the article-level legal design facts required for the transfer, including the 4 percent discount rate, mortality tables, independent valuation procedure, asset-composition constraint, transfer schedule, extinguishment rule and the 18 annex institutions.

Source correction: the earlier local file `data/raw/legislation/DR_DL127_2011_issue.pdf` was removed because it was the Diário da República issue containing the 2012 Budget Law, not the 31 December 2011 Decree-Law 127/2011 act text. Until a reliable raw PDF endpoint is found for `Diário da República n.º 250-A/2011`, the DL127 rows are marked `official_detail_registered` and cite the official DR detail page.

The registry is a legal reconstruction. It does not yet populate bank-level monetary values for liability present value, assets transferred, cash, Portuguese public debt securities, other assets, independent valuer identity or final adjustments.

## Empirical question

> Did the 2011 transfer leave Social Security or the consolidated public sector with an economically material net burden beyond the assets and financing received, and who captured the corresponding benefit?

## Required ledgers

### Transaction-at-inception ledger

```text
bank
pension_fund
pensioners_transferred
liability_pv_reported
asset_value_transferred
cash_transferred
public_debt_transferred
other_assets_transferred
valuation_date
legal_discount_rate
mortality_table
independent_valuer
final_adjustment
```

### Long-run annual ledger

```text
year
state_specific_transfer
special_regime_pension_expenditure
administrative_cost
investment_income_attributable
bank_worker_rgss_contributions
residual_financing_gap
```

## Competing explanations

A. The transaction was close to actuarially neutral at inception and the State fully financed subsequent pension expenditure, leaving no material uncompensated burden on Social Security.

B. The transaction was formally balanced under the 4% valuation assumption but economically adverse under realised longevity/returns or alternative defensible assumptions.

C. The transaction was neutral for Social Security but adverse or beneficial for consolidated general government because of fiscal-accounting and financing effects.

D. The principal effect was distributional: participating banks exchanged long-duration pension liabilities for transferred assets while the public sector assumed longevity/return risk.

E. Later public statements describing the funds as "exhausted" may reflect the expected drawdown of a transferred asset pool rather than proof, by itself, of an original loss; the correct test is assets + financing + realised costs under the legal contract.

## Accounting-standard issue

The repository must replicate both treatments:

- ESA-95: the 2011 transaction was recorded as deficit-improving revenue, about 3.5% of GDP according to the European Commission ex-post evaluation.
- ESA-2010: the same operation is treated as a financial transaction with no direct deficit impact.

This accounting discontinuity is itself an important result for the paper.
