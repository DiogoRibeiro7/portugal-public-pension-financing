# Audit employer contributions

Status: `blocked_missing_payroll_and_revenue_data`

This note documents `data/processed/employer_contribution_audit.csv`.

## Audit Design

The audit separates two concepts:

- legal compliance gap: legally due employer contribution minus CGA employer-contribution revenue after timing, arrears, base-definition and perimeter adjustments;
- economic benchmark gap: contribution under a separate benchmark rate minus recorded revenue.

The economic benchmark is not a legal debt.

## Current Evidence

For 2011, `evidence/legal_contribution_registry.csv` records a legal employer rate of 15 percent for each reconstructed CGA employer class. The audit also records a separate 23.75 percent benchmark rate for comparison.

## Limitation

The registered sources do not yet provide employer-class contribution bases, payroll totals, or CGA revenue split isolating employer contributions from worker quotas and other receipts. As a result, neither legal due amounts nor economic benchmark amounts are computed.

Rows in the audit table are therefore blocked. No legal compliance gap is calculated, and no economic benchmark gap is presented as a debt.

## Validation

`python -m portugal_pensions.cli validate-evidence` validates the employer contribution audit table. Rows marked `complete` must carry both legal and economic benchmark quantities. Every row must state that the benchmark is not a legal debt.
