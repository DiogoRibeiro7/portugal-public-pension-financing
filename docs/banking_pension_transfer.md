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

`data/processed/bank_asset_liability_institution_requirements.csv` enumerates
the 18 DL127 participating institutions and records the bank-level valuation,
asset-composition, final-adjustment and cash-flow inputs required before the
statutory equality or discount-rate sensitivity surface can be reproduced. A
larger liability under an alternative discount rate is treated as sensitivity
evidence, not by itself as an underfunding finding.

`evidence/actuarial_identifiability_registry.csv` records which bank-pension
actuarial quantities are point-identifiable, partially identifiable or blocked
from the current public inputs. It separates statutory valuation, discount-rate
sensitivity, longevity sensitivity and indexation sensitivity, and prohibits
synthetic beneficiary microdata from being presented as observed evidence.

`data/processed/bank_transfer_legal_coverage.csv` is the machine-readable
coverage gate for this reconstruction. It maps each required timeline instrument
and DL127 extraction requirement to the registry record IDs that support it, and
keeps the unresolved DL127 raw-PDF acquisition limitation explicit.

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

`data/processed/bank_worker_rgss_contributions.csv` and
`data/processed/bank_worker_legal_population_mapping.csv` keep active-worker
RGSS contribution flows separate from the DL127 pension-fund transfer. Current
rows identify the 2009 new-worker entry route and the 2011 active-worker CAFEB
integration route, but contribution values remain blank until official
population, contribution and account-reconciliation tables are registered.

The annual ledger is now represented in `evidence/bank_special_regime_annual.csv` and
`data/processed/bank_transfer_long_run.csv`. It covers 2012-2025. For 2012,
`data/processed/bank_pension_cost_2012.csv` reconciles the European Commission's
rounded EUR 0.5bn benchmark to the official EUR 516.0m banking substitute-regime
pension-payment execution reported by Tribunal de Contas. Later annual financing
components remain blank with blocked statuses until official annual account tables are
extracted. Missing values in this ledger are not zeros.

## BPN Separate Case

`data/processed/bpn_2012_pension_transfer.csv` keeps Decree-Law 88/2012 separate
from the 2011 Decree-Law 127/2011 transfer. DL88 assigns the covered BPN-group
responsibilities to CGA, with ISS/CNP handling payment of amounts communicated by
CGA, and requires EUR 96.768004m from the BPN pension fund to be transferred to
CGA. It also identifies EUR 7.319430m for SAMS contribution responsibilities retained
outside the CGA transfer.

The main 2011 private-bank panel excludes BPN unless a broader perimeter is explicitly
defined. The current BPN ledger is a bounded reconstruction: it records the legal
transfer amount and 2012 Tribunal de Contas account extracts but not the full
actuarial valuation or post-2012 drawdown path.

## Competing explanations

A. The transaction was close to actuarially neutral at inception and the State fully financed subsequent pension expenditure, leaving no material uncompensated burden on Social Security.

B. The transaction was formally balanced under the 4% valuation assumption but economically adverse under realised longevity/returns or alternative defensible assumptions.

C. The transaction was neutral for Social Security but adverse or beneficial for consolidated general government because of fiscal-accounting and financing effects.

D. The principal effect was distributional: participating banks exchanged long-duration pension liabilities for transferred assets while the public sector assumed longevity/return risk.

E. Later public statements describing the funds as "exhausted" may reflect the expected drawdown of a transferred asset pool rather than proof, by itself, of an original loss; the correct test is assets + financing + realised costs under the legal contract.

`data/processed/bank_benefit_risk_distribution.csv` separates these channels from a
net-subsidy claim. The current ledger records legal risk movement and aggregate public-account
extracts, but bank-level net positions remain blocked until liability, asset and retained-benefit
values are acquired for each participating institution.

## Debt and financing effects

`data/processed/bank_transfer_debt_financing_effects.csv` records the 2011 financing
resource separately from the later pension-payment obligation. On the observed EUR
3263.1m asset-title receipt recorded in CGE 2011, Banco de Portugal 2012 borrowing-cost
anchors imply potential annual interest savings of EUR 84.8406m at 2.6 percent, EUR
120.7347m at 3.7 percent, and EUR 238.2063m at 7.3 percent. These are sensitivity
calculations, not a net welfare result.

`data/processed/bank_asset_trace_controls.csv` keeps the asset-side treatment
bounded. The observed EUR 3263.1m is recorded as a State financing-resource row,
not as a ring-fenced Social Security or FEFSS asset pool. Cash, Portuguese
public-debt securities, other assets and post-transfer disposal or consolidation
remain blocked until primary Treasury, debt-management or transfer-schedule
records support them.

The gross-debt and consolidated public-finance classification remains unresolved until
the final cash, public-debt-security, and other-asset composition is known and can be
matched to the pension-obligation lifecycle.

## Accounting-standard issue

The repository must replicate both treatments:

- ESA-95: the 2011 transaction was recorded as deficit-improving revenue, about 3.5% of GDP according to the European Commission ex-post evaluation.
- ESA-2010: the same operation is treated as a financial transaction with no direct deficit impact.

`data/processed/bank_esa_treatment_bridge.csv` now records a checked bridge for this discontinuity. It reconciles the CGE 2011 amount of EUR 5993.2m to the 3.5 percent of GDP ESA-95 effect and separately records the ESA-2010 no-direct-deficit-impact classification from the Commission source. Full independent restatement from national-accounts bridge tables remains an open data-quality item.
