# Write manuscript draft

Instruction file: `prompts/18_write_paper.md`
Date: 2026-08-19
Updated: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the article-evidence gate, falsification report and current manuscript scaffold.
- Replaced the placeholder manuscript with a bounded draft that uses only validated article evidence.
- Added explicit manuscript labels for legal fact, accounting fact, interpretation, unresolved evidence, counterfactual result and actuarial assumption.
- Added source-level article-evidence references for every currently supported article-evidence row.
- Added validation that the manuscript references article evidence and keeps evidence-boundary language.
- Added tests for repository manuscript validity and missing evidence references.
- Added `evidence/manuscript_section_boundaries.csv` to gate section-level labels, evidence references, dependency gates and blocked overclaim classes.
- Revised the bounded manuscript prose for clearer framing, transitions and accounting-perimeter
  distinctions without adding unsupported claims.
- Recompiled `paper/manuscript.pdf` from the revised source and synchronized the loaded-language
  audit ledger.
- Added an evidence-and-validation method section tied to the manuscript section-boundary gate.
- Added a related-work and contribution section tied to the bounded literature map.
- Added a research-questions section tied to the analysis protocol and missing-input boundary.

## Result

Created and revised a bounded manuscript draft. It reports extracted and replicated evidence only,
and it explicitly blocks remittance-loss, employer-underpayment, post-2006 reallocation,
combined-balance, bank-subsidy and lifecycle-cost conclusions until required inputs are registered.

## Current Stop Condition

Completion beyond this bounded draft requires the unresolved source work recorded in the falsification report, article-evidence gate, manuscript section-boundary gate and data-quality registry.

## Validation

This branch ran repository validation and full quality checks after regenerating `MANIFEST.sha256`.
