# Data Extraction Roadmap

Status: `partial_bounded_reconstruction`

This roadmap is an extraction inventory for the data still needed to answer the
core research question: how the Social Security budget contributed to Portugal's
State Budget or general-government balance. Boundary modules are included, but
they are ranked after the core public-finance spine.

Current coverage-matrix baseline:

- 31 registered sources acquired as usable raw evidence.
- 6 registered sources still lack usable raw evidence.
- 396 open coverage rows require extraction, backfill, provisional-series
  review, or accounting-boundary resolution.
- 208 of those rows are directly marked `not_extracted`.
- 42 rows already have `partial_extraction`, mostly CGA annual-report rows for
  2011-2024.

## 1. Source Recovery Required Before Extraction

These 6 registered sources must be recovered as citable raw evidence or replaced
with accepted official alternates:

- `BDP_ESA2010_SERIES`: Banco de Portugal ESA2010 statistical-series evidence.
- `DR_DL127_2011`: citable decree text or PDF.
- `DR_LEI60_2005`: citable law text or PDF.
- `DR_EA_CONSOLIDATED`: citable consolidated Estatuto da Aposentacao text or PDF.
- `DR_LEI64_1977`: citable law text or PDF.
- `TC_PCGE_2024`: citable Tribunal de Contas opinion text or PDF.

Recovered on 2026-08-28 as catalogue anchors:

- `DGO_CGE_ARCHIVE`: official Conta Geral do Estado archive page captured and
  hashed under `data/raw/source_catalogues/`.
- `DGO_OE_ARCHIVE`: official State Budget archive page captured and hashed
  under `data/raw/source_catalogues/`.

These recovered routes still require year-level document extraction before they
can support quantitative bridge values.

Gate for each recovered source: update `evidence/source_registry.csv`,
`evidence/source_acquisition_log.csv`, `evidence/data_license_registry.csv`,
store the raw file under `data/raw/`, record SHA-256, and pass
`python -m portugal_pensions.cli validate-evidence`.

## 2. Core Spine: Surplus Contribution Bridge

This block comes first because it directly answers the repository's central
question.

### CGE Public Accounts

- Coverage rows: 49 `not_extracted`.
- Years: 1977-2025.
- Source route: primarily `DGO_CGE_ARCHIVE`, with `DR_LEI64_1977` relevant to
  the 1977 definition break.
- Extract:
  - State Budget balance and execution aggregates;
  - general-government balance where reported or bridged;
  - revenue, expenditure, current/capital split where needed;
  - transfers to Social Security and CGA;
  - one-off operations affecting headline balance;
  - notes on definition breaks, perimeter changes, and accounting basis.
- Target outputs:
  - `data/processed/state_budget_surplus_bridge.csv` or equivalent;
  - `evidence/extraction_audit.csv`;
  - `evidence/reconciliation_log.csv`;
  - source-specific notes in `docs/state_financing_history.md`.

### Social Security Accounts

- Coverage rows: 49 `not_extracted`.
- Years: 1977-2025.
- Source route: Social Security account publications and `IGFSS_CSS_ARCHIVE`.
- Extract:
  - Social Security revenue;
  - contributions;
  - expenditure;
  - pension expenditure;
  - current balance;
  - overall budget/account balance;
  - State transfers received;
  - transfers or financing flows returned to the State, where present;
  - FEFSS-related flows where they affect the budget balance.
- Target outputs:
  - Social Security annual account ledger;
  - Social Security contribution-to-surplus bridge;
  - `evidence/extraction_audit.csv`;
  - `evidence/reconciliation_log.csv`.

### State Budget Documents

- Coverage rows: 30 `not_extracted` for 1996-2025.
- Additional rows: 19 `not_assessed` for 1977-1995.
- Source route: `DGO_OE_ARCHIVE` and year-level State Budget documents.
- Extract:
  - budgeted transfers to Social Security;
  - budgeted transfers to CGA;
  - initial and amended appropriations where relevant;
  - execution-versus-budget comparison fields;
  - wording that identifies extraordinary or compensatory transfers.
- Target outputs:
  - budgeted transfer ledger;
  - bridge between OE authorizations and CGE/CSS execution;
  - extraction audit rows for each extracted table.

### Primary Bridge Dataset

Create the central dataset after the three ledgers above exist.

- Required fields:
  - year;
  - State Budget or general-government balance;
  - Social Security account balance;
  - gross State transfers to Social Security;
  - net Social Security contribution to headline balance;
  - CGA transfer adjustment, if included in the perimeter;
  - one-off operation flags;
  - accounting basis;
  - perimeter;
  - source IDs;
  - reconciliation residual;
  - claim-permitted status.
- Gate: no conclusion about Social Security's contribution to surplus until the
  bridge reconciles or the residual is explicitly blocked.

## 3. Public Employment and Worker-Flow Inputs

This block explains mechanisms behind contribution flows. It should not delay
the core bridge unless the manuscript makes cohort or payroll claims.

### Public Employment Counts

- Coverage rows: 34 `not_extracted` for 1977-2010.
- Additional rows: 15 `provisional_possible` for 2011-2025.
- Extract:
  - public-sector employment counts;
  - series definitions and perimeter;
  - first reliable official series boundary;
  - breaks between SIEP, BOEP, INE, and account-based sources.
- Target outputs:
  - public employment count ledger;
  - uncertainty registry entries for definition breaks.

### Public-Worker Cohort Inputs

- Coverage rows: 19 `not_extracted` for 2006-2025.
- Additional row: 1 `provisional_possible` for 2011.
- Extract:
  - new public-worker entrant counts after the CGA closure;
  - contribution base payroll;
  - RGSS employee and employer rates;
  - mapping from worker cohort to Social Security contributions;
  - exclusions by perimeter or contingency coverage.
- Target outputs:
  - public-worker RGSS cohort ledger;
  - contribution-flow bridge;
  - counterfactual input table.

## 4. CGA Financing Support Module

This block supports pension-boundary claims and separates CGA financing from
the Social Security surplus question.

### CGA Annual Accounts

- Coverage rows: 9 `not_extracted` for 2002-2010.
- Additional rows: 26 `not_assessed` for 1977-2001 and 2025.
- Already partial: 14 years for 2011-2024.
- Extract:
  - worker quotations;
  - employer contributions;
  - State Budget transfers;
  - other public transfers;
  - investment income;
  - pension expenditure;
  - other benefits;
  - administration;
  - contributor count;
  - pensioner count;
  - contribution-base payroll where available.
- Target outputs:
  - `data/processed/cga_financing_ledger.csv`;
  - `evidence/extraction_audit.csv`;
  - `docs/cga_financing_reconstruction.md`.

### CGA Subscriber and Pensioner Counts

- Coverage rows: 9 `not_extracted` for 2002-2010.
- Additional rows: 26 `not_assessed` for 1977-2001 and 2025.
- Already partial: 14 years for 2011-2024.
- Extract:
  - subscribers;
  - aposentados/reformados;
  - survival pensionists;
  - other pensionists;
  - ratios reported in source tables.
- Gate: keep aposentados/reformados separate from other pensioner categories
  unless the source explicitly defines a combined total.

### CGA Employee and Employer Revenue Split

- Coverage rows: 9 `not_extracted` for 2002-2010.
- Additional rows: 26 `not_assessed` for 1977-2001 and 2025.
- Already partial: 14 years for 2011-2024.
- Extract:
  - worker quotas;
  - employer/entity contributions;
  - arrears or regularization lines, if separately reported;
  - mapping from source labels to comparable ledger fields.

## 5. Legal Contribution Rule Backfill

- Coverage rows: 44 `requires_primary_law_backfill` for 1977-2025.
- Extract:
  - legal employee contribution rates;
  - legal employer contribution rates;
  - effective dates;
  - employer-class variation;
  - contingency scope;
  - transition rules;
  - source articles and consolidated-law references.
- Target outputs:
  - `data/processed/legal_contribution_rules.csv`;
  - employee remittance audit inputs;
  - employer contribution audit inputs;
  - source registry and extraction audit rows.

Gate: do not infer non-compliance from rate rules alone. Payroll bases and
recorded receipts must be extracted separately.

## 6. Banking Pension Transfer Boundary Module

This block matters for one-off public-account effects and for avoiding false
classification of bank-transfer effects as ordinary Social Security surplus.

### Bank Asset/Liability Transfer Schedules

- Coverage rows: 2 `requires_valuation_schedule` for 2011-2012.
- Coverage rows: 13 `requires_cashflow_schedule` for 2013-2025.
- Extract:
  - transferred pension assets;
  - transferred liabilities;
  - actuarial assumptions;
  - cash-flow schedules;
  - State financing transfers to Social Security;
  - pension payments made under the substitute regime;
  - administrative or timing adjustments.
- Target outputs:
  - bank asset-liability audit;
  - bank pension cost ledger;
  - bank long-run financing ledger;
  - flow-of-funds bridge rows.

### Banking Legal Sources

- Registered source recovery still required for `DR_DL127_2011`.
- Extract:
  - responsibilities assumed by Social Security;
  - assets transferred to the State;
  - State financing obligation;
  - extinguishment of bank responsibilities;
  - separation from BPN/CGA treatment under `DR_DL88_2012`.

## 7. ESA and Accounting-Treatment Resolution

- Coverage rows: 5 `ESA95_ESA2010_conflict` for 2010-2014.
- Coverage rows: 11 `ESA2010_basis` for 2015-2025.
- Source recovery still required for `BDP_ESA2010_SERIES`.
- Extract or resolve:
  - ESA-95 treatment of the 2011 bank pension-fund transfer;
  - ESA-2010 reclassification;
  - Banco de Portugal bridge or statistical-series note;
  - European Commission confirmation where relevant;
  - effect on deficit/surplus and debt measures.
- Target outputs:
  - ESA treatment bridge;
  - reconciliation log rows;
  - manuscript boundary language.

Gate: distinguish cash-budget effects, national-account deficit effects, and
gross-debt classification before using any figure in the surplus bridge.

## 8. Suggested Work Order

1. Use the recovered `DGO_CGE_ARCHIVE` and `DGO_OE_ARCHIVE` catalogues to
   acquire year-level CGE and State Budget documents; recover remaining legal,
   Banco de Portugal, Tribunal de Contas, and Social Security annual-account
   routes or year-level PDFs.
2. Extract 1996-2025 CGE, Social Security, and State Budget values first, since
   these years are more likely to have structured annual documents.
3. Build the first Social Security contribution-to-surplus bridge for the
   highest-coverage years only.
4. Backfill 1977-1995 public accounts and document definition breaks.
5. Extract CGA 2002-2010 annual reports and finish the CGA historical gap.
6. Backfill legal contribution rules and public-worker cohort inputs only where
   needed for contribution-flow claims.
7. Resolve banking transfer cash-flow and ESA-treatment rows for one-off
   accounting adjustments.
8. Promote manuscript claims only after each required value has a source ID,
   audit row, unit, accounting basis, perimeter, and residual status.

## 9. Completion Gates

The extraction roadmap is complete only when:

- the 6 missing registered sources are recovered or formally superseded;
- the 208 `not_extracted` rows are either extracted or converted to explicit
  blockers with source-backed reasons;
- the 97 `not_assessed` rows are assessed and either extracted, blocked, or
  marked not applicable with justification;
- provisional public-employment and cohort rows are promoted or rejected;
- ESA and bank-transfer boundary rows have explicit accounting treatment;
- every quantitative claim used in the manuscript traces to a processed dataset,
  source ID, extraction audit row, unit, perimeter, and accounting basis;
- `make quality` passes on a clean checkout.
