# Build legal contribution history

Instruction file: `prompts/02_build_legal_contribution_history.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved the existing 2006-forward legal-rate registry grounded in official judicial summaries and the current consolidated statute.
- Tightened validation for source IDs, controlled statuses, required employer classes, one open interval per class, interval direction, covered risks, CGA quota base wording, component totals, duplicate keys and overlapping periods.
- Registered the legal-rate history as a source-registered quantitative legal claim, not as a fully replicated primary-law extraction.
- Preserved existing validated outputs and did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added an executable bounded legal-rate history gate. The current registry supports a 2006-forward reconstruction by employer class while keeping the pre-2006 and direct budget-law article backfill unresolved.

## Current Stop Condition

Completion beyond this record requires direct article-level extraction and hashing for historical budget laws and a complete pre-2006 rate history. Until those inputs exist, the table remains a bounded official-summary reconstruction and cannot be treated as a complete primary-legislation rate panel.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
