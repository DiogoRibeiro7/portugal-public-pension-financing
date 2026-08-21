# Build literature map

Instruction file: `prompts/43_literature_review_and_novelty_map.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Ran a bounded web-indexed literature and institutional-source search on
  Portuguese pension financing, CGA reform, CGA financial analysis, pension
  expenditure determinants, financialisation, bank pension transfers, and ESA
  pension accounting.
- Rebuilt `evidence/literature_map.csv` with source category, topic, research
  question, method, period, data, finding, relation to this project, inclusion
  decision, search channel, query, search date, and source URL.
- Replaced the placeholder search protocol with a dated bounded protocol.
- Added `docs/related_work_synthesis.md` with nearest-neighbour and bounded
  contribution language.
- Added a validation gate for the literature map and related-work novelty rule.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a sourced bounded literature and novelty map. The current nearest
neighbours cover CGA reform simulation, long-run pension projections,
macroeconomic pension-expenditure determinants, CGA financial analysis,
financialisation context, and ESA/national-accounts pension accounting.

## Current Stop Condition

Completion beyond this record requires a dedicated database search in Scopus,
Web of Science, EconLit, Google Scholar, and Portuguese library catalogues.
Until that is done, the map supports cautious bounded contribution language
only.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` and `make quality`
after regenerating `MANIFEST.sha256`.
