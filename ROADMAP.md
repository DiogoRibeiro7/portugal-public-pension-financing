# Roadmap

Status: partial bounded reconstruction

This repository is not ready for a publication report yet. The immediate priority is still data collection and extraction for the question: how much the Social Security budget contributed to Portugal's State Budget or general-government surplus.

The current manuscript must remain bounded until the core public-finance bridge is source-backed, audited, and reconciled.

## Current State

Baseline after the 2020 public-account extraction:

- Source registry: 41 acquired sources and 6 registered-only sources.
- Source coverage matrix: 198 rows still marked `not_extracted`.
- Source coverage matrix: 97 rows still marked `not_assessed`.
- Source coverage matrix: 52 rows have `partial_extraction`.
- Data quality registry: 45 high-severity open blockers and 18 medium-severity open blockers.
- Public-account extracts completed for 2020, 2021, 2022, 2023, and 2024.
- Raw official files remain local-only unless redistribution terms are verified.

## Manuscript Gate

Start the full manuscript only after these minimum conditions are met:

- A core annual bridge exists for Social Security, State Budget, and general-government balance measures.
- Every value used in the bridge has a source ID, source hash, extraction-audit row, unit, accounting basis, perimeter, and reconciliation status.
- Social Security balances are separated from State transfers received from the State Budget.
- CGA flows are separated from Social Security flows unless a declared combined perimeter is being tested.
- One-off bank-pension-transfer effects are flagged and not treated as ordinary Social Security balance.
- Unresolved source conflicts are carried as ranges or blockers, not silently smoothed.

Until then, the paper can only be a bounded draft describing available evidence and blockers.

## Priority 1: Core Public-Finance Bridge

This is the central work stream.

### 1. CGE Public Accounts

Completed:

- Selected annual public-account balance extracts for 2020-2024.

Outstanding:

- Acquire and extract year-level CGE files for 1977-2019 and 2025 where available.
- Start backward from 2019, then continue 2018, 2017, and so on.
- For each year, extract general-government or public-administration balance, central-government balance, Social Security balance, combined central-government plus Social Security balance, revenue, expenditure, and relevant transfer lines.
- Record definition breaks and accounting-basis changes explicitly.

Target outputs:

- `data/processed/public_account_balance_<year>_extract.csv` for each extracted year.
- Updated `evidence/source_registry.csv`.
- Updated `evidence/source_acquisition_log.csv`.
- Updated `evidence/source_coverage_matrix.csv`.
- Updated `evidence/extraction_audit.csv`.
- Updated `MANIFEST.sha256`.

### 2. Social Security Accounts

Completed:

- Selected Social Security account extracts for 2020-2024 through DGO CGE workbooks.

Outstanding:

- Backfill 1977-2019 and 2025 account values where official files exist.
- Extract total Social Security balance, Previdential balance, Citizenship/Social Protection balance, Special Regimes balance, contributions, effective revenue, effective expenditure, State Budget transfers, banking-pensions transfer lines, and pension expenditure.
- Verify whether older files use euros, thousand euros, escudos, or million euros before normalizing.

Target outputs:

- A long annual Social Security ledger.
- A transfer-adjusted Social Security contribution-to-surplus bridge.
- Reconciliation rows for revenue minus expenditure and subsystem totals.

### 3. State Budget Documents

Outstanding:

- Extract State Budget documents from 1996-2025 using the DGO State Budget archive.
- Locate or document official routes for 1977-1995.
- Extract budgeted transfers to Social Security, budgeted transfers to CGA, amended appropriations, and execution-versus-budget comparison fields.
- Separate ordinary transfers from extraordinary or compensatory transfers.

Target outputs:

- Budgeted-transfer ledger.
- OE-to-CGE execution bridge.
- Year-level extraction audit rows.

## Priority 2: CGA and Public-Pension Boundary

Outstanding:

- Complete CGA annual-account extraction for 2002-2010.
- Assess or recover official CGA routes for 1977-2001 and 2025.
- Extract worker quotas, employer contributions, State transfers, other transfers, pension expenditure, other benefits, administration, contributors, pensioners, survivors, and payroll bases where available.
- Backfill legal contribution rules for 1977-2025 from primary law and budget-law articles.
- Keep legal compliance tests blocked until payroll bases and recorded receipts are extracted.

Target outputs:

- Completed `data/processed/cga_financing_ledger.csv`.
- Completed employee-remittance and employer-contribution audit inputs.
- Updated legal contribution registry with source article references.

## Priority 3: Public-Worker RGSS and FEFSS Inputs

Outstanding:

- Acquire public-worker new-entrant cohort counts after the CGA closure.
- Acquire public-worker contribution bases and applicable RGSS employee/employer rates.
- Acquire official FEFSS annual returns, return definitions, fee treatment, timing conventions, and actual asset stocks.
- Separate actual Social Security/FEFSS flows from counterfactual capitalization flows.

Target outputs:

- Public-worker RGSS cohort ledger.
- Public-worker RGSS contribution-flow bridge.
- FEFSS return series.
- FEFSS capitalization counterfactual with explicit financing assumptions.

## Priority 4: Bank-Pension Transfer Boundary

Outstanding:

- Recover a reliable citable source for `DR_DL127_2011`.
- Acquire bank-level valuation schedules, transferred asset composition, cash/public-debt/other-asset split, final adjustments, and independent valuer information.
- Acquire post-2012 annual Social Security banking-regime pension expenditure, State transfer, administrative cost, asset-income, drawdown, and timing-adjustment components.
- Keep BPN as a separate case unless a source-backed perimeter bridge justifies combining it with the 2011 DL127 panel.

Target outputs:

- Bank asset-liability transfer schedule.
- Bank special-regime annual financing ledger.
- Bank lifecycle and debt-classification bridge.

## Priority 5: ESA and Accounting Treatment

Outstanding:

- Recover or replace `BDP_ESA2010_SERIES`.
- Acquire machine-readable or citable ESA95/ESA2010 restatement evidence for the 2011 bank pension-fund transfer.
- Separate cash-budget effects, national-account deficit effects, and gross-debt classification effects.

Target outputs:

- ESA treatment bridge.
- Updated source conflict registry.
- Manuscript language that distinguishes cash accounting from national accounts.

## Priority 6: Remaining Source Recovery

Registered-only sources still need usable citable raw evidence or an accepted official substitute:

- `BDP_ESA2010_SERIES`
- `DR_DL127_2011`
- `DR_LEI60_2005`
- `DR_EA_CONSOLIDATED`
- `DR_LEI64_1977`
- `TC_PCGE_2024`

For each recovered source:

- Store the raw file locally under `data/raw/`.
- Record SHA-256 in `evidence/source_registry.csv`.
- Add an acquisition-log row.
- Add or update the license-policy row.
- Keep raw files excluded from release archives unless redistribution terms are clear.

## Next Session

Recommended first task:

1. Acquire the 2019 DGO CGE report and companion tables.
2. Extract the same balance and Social Security rows already extracted for 2020-2024.
3. Update source metadata, acquisition log, source coverage, extraction audit, license metadata, and manifest.
4. Run `make quality`.
5. Open and merge a short PR.

Then repeat for 2018, 2017, 2016, and 2015 before deciding whether the bridge is stable enough for an initial analytical table.

## Do Not Do Yet

- Do not cut a new report release.
- Do not claim the manuscript is publication-ready.
- Do not publish raw official files with unclear redistribution terms.
- Do not treat partial extracts as a completed historical panel.
- Do not infer Social Security's net contribution to the State surplus until the transfer-adjusted bridge is built.
