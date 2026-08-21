# Decompose CGA closure

Instruction file: `prompts/47_cga_closed_scheme_demographic_decomposition.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Checked the CGA financing ledger, publication figure companions, data-quality registry, and
  closed-scheme source requirements.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.
- Replaced the empty closed-scheme dataset with a structured decomposition ledger.
- Updated the FIG03 companion CSV to point at the closed-scheme decomposition blockers.
- Added validation and tests for the closed-scheme decomposition ledger.
- Updated the closed-scheme documentation with interpretation boundaries.

## Result

Recorded a bounded closed-scheme decomposition identity and the required missing driver series:
contributor counts, payroll bases, policy rates, pensioner and survivor counts, average benefits,
transfers, and residual reconciliation. No numerical driver effect is reported.

## Current Stop Condition

Completion beyond this record requires annual CGA contributor counts, pensioner and survivor counts,
contribution payroll bases, component contribution revenues, pension expenditure, transfer
components, and a reconciled stock-flow identity. Until those inputs exist, causal attribution to
closure or prior financing choices remains blocked under the repository evidence rules.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` after regenerating `MANIFEST.sha256`.
