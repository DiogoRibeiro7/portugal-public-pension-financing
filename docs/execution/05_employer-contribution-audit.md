# Audit employer contributions

Instruction file: `prompts/05_employer_contribution_audit.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Expanded the employer contribution audit to a 1977-2025 grid across the four
  reconstructed CGA employer classes.
- Added bounded class/year legal employer rates where the legal contribution
  registry supports them.
- Kept payroll bases, recorded CGA employer revenue, timing, arrears, base and
  perimeter adjustments as missing inputs rather than substituting zeros.
- Added validation for year/class coverage, source IDs, blocked-input lists,
  no-claim flags, and separate complete-row legal and economic gap arithmetic.

## Result

Added an executable employer contribution audit gate.

## Current Stop Condition

Completion beyond this bounded audit requires employer-class payroll bases, CGA
employer-contribution revenue splits, timing and arrears corrections,
contribution-base adjustments, perimeter adjustments, and pre-2006 primary legal
rate history. Until then no legal compliance gap or economic benchmark gap is
quantified.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
