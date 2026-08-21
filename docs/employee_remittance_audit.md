# Audit employee remittances

Status: `partial_bounded_reconstruction`

This note documents `data/processed/employee_remittance_audit.csv`.

## Audit Design

The audit now contains one row for every study year from 1977 through 2025.
Rows are explicit blockers unless all quantities needed for a remittance
reconciliation have been extracted.

The audit separates three quantities that must not be conflated:

- legal worker liability, computed from the statutory worker quota and the legally relevant contribution base;
- payroll amount actually withheld from workers;
- CGA revenue recorded as subscriber quotas.

For 2006 onward, the bounded legal contribution registry supplies worker quota
rates where currently registered. CGA's organic statute records that CGA
controls subscriber quotas and employer contributions and that subscriber quotas
are own revenue. Years before the bounded legal-rate evidence remain blocked
for primary legal-rate extraction as well as payroll and revenue data.

## Limitation

The registered sources do not yet provide:

- total payroll amounts actually withheld from workers for CGA;
- CGA revenue split isolating worker quotas from employer contributions and other contribution-like receipts;
- timing, arrears, correction, contribution-base and perimeter adjustments.

The current rows are therefore blocked. No unexplained remittance gap is
calculated, and no claim is made that deducted worker amounts were not remitted.

## Validation

`python -m portugal_pensions.cli validate-evidence` validates the remittance
audit table. Rows marked `complete` must include legal liability, payroll
withholding, recorded CGA worker revenue, adjustments, and an unexplained
residual. Blocked rows must carry source IDs, missing-input lists, no-claim
flags, and notes that avoid remittance-gap claims.
