# Audit employee remittances

Status: `blocked_missing_payroll_and_revenue_data`

This note documents `data/processed/employee_remittance_audit.csv`.

## Audit Design

The audit separates three quantities that must not be conflated:

- legal worker liability, computed from the statutory worker quota and the legally relevant contribution base;
- payroll amount actually withheld from workers;
- CGA revenue recorded as subscriber quotas.

For 2011, the legal worker quota rate is recorded as 11 percent from the official legal-history evidence. CGA's organic statute records that CGA controls subscriber quotas and employer contributions and that subscriber quotas are own revenue.

## Limitation

The registered sources do not yet provide:

- total payroll amounts actually withheld from workers for CGA;
- CGA revenue split isolating worker quotas from employer contributions and other contribution-like receipts;
- timing, arrears, correction, contribution-base and perimeter adjustments.

The current row is therefore blocked. No unexplained remittance gap is calculated, and no claim is made that deducted worker amounts were not remitted.

## Validation

`python -m portugal_pensions.cli validate-evidence` validates the remittance audit table. Rows marked `complete` must include legal liability, payroll withholding, recorded CGA worker revenue, adjustments, and an unexplained residual. Blocked rows must carry source IDs and notes.
