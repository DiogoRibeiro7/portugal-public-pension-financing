# Data and code availability

This repository is a bounded research snapshot, not a final public-report release.

## Code

The analysis code, validation code, tests, evidence registries, manuscript source, bounded
manuscript PDF, and release readiness artifacts are tracked in the Git repository. The current
archive checksum contract is `MANIFEST.sha256`.

## Public raw sources

Acquired public raw sources are stored under `data/raw/` and registered in
`evidence/source_registry.csv` with SHA-256 hashes. Registered sources without immutable raw files
remain labelled as `registered` rather than `acquired`.

## Derived data

Derived and intermediate research files are stored in:

- `data/interim/`
- `data/processed/`
- `evidence/`
- `paper/figures/data/`
- `paper/tables/`

Every manuscript-facing claim must pass `evidence/article_evidence.csv` and the repository
validation gate before use.

## Restricted or incomplete inputs

The current package does not include a complete source chain for CGA component ledgers, payroll
withholding records, employer payroll bases, public-worker RGSS cohort flows, bank-level transfer
schedules, actuarial cash-flow paths, post-2012 State-specific bank-pension financing, or complete
combined-balance inputs.

These gaps are recorded in `evidence/data_quality_registry.csv`,
`data/processed/release_reproducibility_audit.csv`, and `docs/reproducibility_report.md`.

## Reuse boundary

The current manuscript is reproducible only for the bounded claims listed in
`evidence/article_evidence.csv`. The compiled PDF is a bounded review artifact only. It should not
be cited as establishing employee remittance losses, employer underpayment amounts, post-2006
reallocation magnitudes, bank-transfer subsidy, or lifecycle public-finance gain or loss.
