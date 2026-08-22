# Audit claim language

Status: `partial_bounded_reconstruction`

The current manuscript has been audited against legally and politically loaded terms. The
machine-readable audit is `data/processed/manuscript_claim_language_audit.csv`, with section
coverage checked against `evidence/manuscript_section_boundaries.csv`.

## Current Result

The manuscript uses loaded terms only in bounded accounting, unresolved-evidence, or explicitly
negated contexts. The audit covers:

- `debt`
- `underfunded`
- `diverted`
- `subsidy`
- `loss`
- `losses`
- `harmful`
- `surplus`
- `deficit`
- `sustainable`
- `artificial`

## Boundary

The current manuscript does not state that CGA was underfunded, that deductions were diverted, that
the banking transfer was a subsidy, that Social Security suffered a lifecycle loss, that current
surpluses are artificial, or that any institution is sustainable on an actuarial basis.

Permitted uses are tied to defined accounting concepts, article-evidence rows, and unresolved
evidence language. Present loaded terms must also map to manuscript section-boundary IDs. Any future
manuscript use of these terms must update the audit ledger and pass validation.

## Evidence Rule

This file records the current executable state only. It must not be read as a completed
quantitative finding until the required sources, extraction records, transformations, and checks
are present.
