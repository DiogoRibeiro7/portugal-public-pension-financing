# Generate article evidence

Instruction file: `prompts/17_generate_article_evidence.md`
Date: 2026-08-19
Updated: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the claim registry, publication artifact registries and current manuscript scaffold.
- Added `evidence/article_evidence.csv` and `evidence/article_evidence.md` mapping supported article numbers to source IDs, raw values, transformations, processed datasets and output artifacts.
- Added evidence-level `figure_registry.csv` and `table_registry.csv` with article-use status for publication artifacts.
- Added validation that material quantitative/accounting claims have article evidence and that blocking claim statuses cannot pass the article gate.
- Added tests for repository article evidence and blocking-claim rejection.
- Added `evidence/article_evidence_claim_boundaries.csv` to gate permitted article use and blocked inferences for every article-evidence row.

## Result

Implemented a bounded article-evidence gate for currently supported extracted and replicated claims. The gate supports caveated article use only; it does not authorize unresolved lifecycle, causal or combined-balance claims.

## Current Stop Condition

Completion beyond this bounded gate requires the still-missing processed series and source work recorded in the data-quality registry. Any future material claim with `to_replicate`, `unresolved`, missing provenance, missing claim boundary or unsupported output artifact must block article generation.

## Validation

This branch ran repository validation and full quality checks after regenerating `MANIFEST.sha256`.
