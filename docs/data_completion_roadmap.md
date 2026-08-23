# Data Completion Roadmap

Status: `partial_bounded_reconstruction`

This roadmap separates two different gaps: source acquisition gaps and
year-variable extraction gaps. The current baseline has 29 acquired registered
sources, 8 registered sources still missing usable raw evidence, and 208
coverage-matrix rows still marked `not_extracted`.

## Priority 1: Recover Missing Registered Sources

Goal: turn the 8 registered-but-not-acquired sources into usable, hashed raw
evidence or document a final alternate route.

- `DGO_CGE_ARCHIVE`: recover a stable Conta Geral do Estado archive route or
  year-level CGE PDFs.
- `DGO_OE_ARCHIVE`: recover a stable State Budget archive route or year-level
  budget PDFs.
- `BDP_ESA2010_SERIES`: recover Banco de Portugal ESA2010 statistical-series
  evidence or an official archived equivalent.
- `DR_DL127_2011`: replace shell HTML with citable decree text or PDF.
- `DR_LEI60_2005`: replace shell HTML with citable law text or PDF.
- `DR_EA_CONSOLIDATED`: replace shell HTML with citable consolidated statute
  text or PDF.
- `DR_LEI64_1977`: replace shell HTML with citable law text or PDF.
- `TC_PCGE_2024`: replace shell HTML with citable Tribunal de Contas opinion
  text or PDF.

Completion gate: every recovered source must be registered in
`evidence/source_registry.csv`, logged in `evidence/source_acquisition_log.csv`,
covered in `evidence/data_license_registry.csv`, stored under `data/raw/`, and
validated by `python -m portugal_pensions.cli validate-evidence`.

## Priority 2: Finish CGA Historical Extraction

Goal: close the near-term CGA gap before broader public-account extraction.

- Acquire and hash CGA annual reports for 2002-2010 where available.
- Extract worker quotations, employer contributions, State Budget transfers,
  pension expenditure, other benefits, subscribers, and retirees for 2002-2010.
- Update `data/processed/cga_financing_ledger.csv`,
  `evidence/extraction_audit.csv`, and `docs/cga_financing_reconstruction.md`.
- Preserve unresolved blockers for other public transfers, investment income,
  administration, and payroll until source tables support them.

Current uncovered CGA block: 27 `not_extracted` rows across 2002-2010 for
annual accounts, subscriber/pensioner counts, and employee/employer revenue
split.

## Priority 3: Build Core Public-Accounts Backbone

Goal: make the manuscript's historical finance claims depend on extracted
official accounts instead of route-only blockers.

- CGE public accounts: extract registered values for 1977-2025 where available.
- Social Security accounts: extract account values for 1977-2025 where
  available.
- State Budget documents: extract budget-transfer and appropriation values for
  1996-2025.

Current uncovered blocks: 49 CGE rows, 49 Social Security rows, and 30 State
Budget rows.

## Priority 4: Public-Worker Inputs

Goal: reduce the remaining uncertainty in public-worker reallocation and
contribution-flow estimates.

- Public employment counts: backfill 1977-2010 or document the first reliable
  official series boundary.
- Public-worker cohort inputs: resolve 2006-2025 new-entrant counts,
  contribution bases, and rate mapping.
- Connect each resolved input to the remittance, employer-contribution, and
  counterfactual ledgers.

Current uncovered block: 53 rows across public employment counts and
public-worker cohort inputs.

## Priority 5: Manuscript Readiness Gate

Start a full manuscript drafting pass only after the data gates below are true:

- all 8 registered source gaps are resolved or explicitly replaced by accepted
  alternate official sources;
- CGA 2002-2024 has extracted annual-report components where source tables
  allow it;
- CGE, Social Security, and State Budget extraction coverage is sufficient for
  the paper's main tables and figures;
- remaining missing values are represented as explicit blockers, not zeros or
  inferred estimates;
- `make quality` passes on a clean checkout.

Until then, manuscript work should be limited to bounded wording, claim
inventory, figure/table scaffolding, and methods text that accurately describes
the current source limits.
