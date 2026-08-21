# Audit employer contributions

Status: `partial_bounded_reconstruction`

This note documents `data/processed/employer_contribution_audit.csv`.

## Audit Design

The audit separates two concepts:

- legal compliance gap: legally due employer contribution minus CGA employer-contribution revenue after timing, arrears, base-definition and perimeter adjustments;
- economic benchmark gap: contribution under a separate benchmark rate minus recorded revenue.

The economic benchmark is not a legal debt.

## Current Evidence

The audit now contains one row for each study year from 1977 through 2025 and
for each reconstructed CGA employer class. Where the bounded legal contribution
registry identifies a class/year legal employer rate, the row records that rate.
Where legal history is not yet extracted, the row remains blocked for primary
law backfill.

Rows with legal rates also carry a separate 23.75 percent economic benchmark
where applicable. That benchmark is a counterfactual comparison only and is not
a legal debt.

## Limitation

The registered sources do not yet provide employer-class contribution bases,
payroll totals, or CGA revenue split isolating employer contributions from
worker quotas and other receipts. As a result, neither legal due amounts nor
economic benchmark amounts are computed.

Rows in the audit table are therefore blocked. No legal compliance gap is
calculated, and no economic benchmark gap is presented as a debt.

## Validation

`python -m portugal_pensions.cli validate-evidence` validates the employer
contribution audit table. Rows marked `complete` must carry both legal and
economic benchmark quantities and reconcile both residuals. Blocked rows must
carry source IDs, missing-input lists, no-claim flags and the statement that the
benchmark is not a legal debt.
