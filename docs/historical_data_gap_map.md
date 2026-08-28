# Historical Data Gap Map

Status: `partial_bounded_reconstruction`

Coverage matrix: `evidence/source_coverage_matrix.csv`

Search date: 2026-08-21

## Horizon

The matrix represents every year from 1977 through 2025 for 12 core variables:

- `cge_public_accounts`
- `state_budget_documents`
- `cga_reports_accounts`
- `cga_subscriber_pensioner_counts`
- `cga_employee_employer_revenue_split`
- `social_security_accounts`
- `public_employment_counts`
- `public_worker_cohort_inputs`
- `legal_contribution_rules`
- `bank_pension_transfer_legal`
- `bank_asset_liability_transfer_schedules`
- `esa_pension_transfer_treatment`

Every row is classified as one of `observed`, `unavailable`,
`definition-break`, `revision-conflict`, or `not-applicable`.

## Official Source Anchors

The bounded source pass registered official catalogue anchors for:

- DGO Conta Geral do Estado archive.
- DGO State Budget archive.
- CGA annual reports.
- IGFSS Social Security budget and account page.
- DGAEP SIEP and BOEP public-employment statistics.
- Diario da Republica legal texts.
- INE historical publications.
- Banco de Portugal ESA2010 statistical-series release.

The DGO CGE and State Budget catalogue anchors, CGA annual-report anchors, and
IGFSS Social Security budget/account page are acquired raw evidence, but they
are still route-level sources for many rows. Rows marked `observed` mean that an
official route or already acquired official source was identified for that
variable-year. They do not mean the relevant table has already been downloaded,
hashed, extracted, and reconciled.

## Main Breaks

The matrix records these current breaks:

- 1977: CGE statutory perimeter change from Lei n.o 64/77.
- 1996: modern DGO budget-document archive route begins.
- 2006: CGA closed to new subscribers and new public workers move to RGSS.
- 2011: bank pension-transfer framework and DGAEP SIEP public-employment series
  start point.
- 2010-2014: ESA95/ESA2010 pension-transfer treatment conflict window.

## Current Gaps

The largest unresolved gaps are:

- pre-2002 CGA annual financial and statistical accounts;
- year-level Social Security account availability outside the currently
  observed 2012 and 2024 anchors;
- pre-2011 harmonized public-employment counts;
- post-2006 new-public-worker cohort inputs rather than aggregate employment;
- bank-level asset, liability, valuation, and lifecycle cash-flow schedules;
- primary legal backfill for all CGA/RGSS contribution rates.

Secondary estimates may be used later only as cross-checks. They must not fill
primary-source gaps in the reconstruction ledger.
