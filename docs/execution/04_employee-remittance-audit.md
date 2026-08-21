# Audit employee remittances

Instruction file: `prompts/04_employee_remittance_audit.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Expanded the employee remittance audit to one row for each year from 1977
  through 2025.
- Added bounded legal worker quota rates where the registered legal contribution
  history supports them.
- Kept payroll withholding, CGA worker-quota revenue, timing, arrears, base and
  perimeter adjustments as missing inputs rather than substituting zeros.
- Added validation for year coverage, source IDs, blocked-input lists, no-claim
  flags and complete-row remittance-gap arithmetic.

## Result

Added an executable employee remittance audit gate.

## Current Stop Condition

Completion beyond this bounded audit requires payroll withholding records, CGA
worker-quota revenue split, timing and arrears corrections, contribution-base
adjustments and perimeter adjustments. Until then no remittance-loss conclusion
is supported.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
