# Generate figures and tables

Instruction file: `prompts/16_generate_figures_and_tables.md`
Date: 2026-08-19
Updated: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with available processed CSVs, paper artifacts and repository validation code.
- Added one companion CSV for each of the eleven required figure candidates under `paper/figures/data/`.
- Added `paper/figures/figure_registry.csv` to record source datasets, publication status and blockers.
- Added publication table companions for falsification status and open data-quality blockers.
- Added validation that all required figure candidates are represented, companion CSVs exist and ready figures use processed source datasets.
- Added tests for repository publication artifacts and required figure coverage.
- Added `evidence/publication_artifact_readiness_requirements.csv` to gate blocked and partial figure/table use.

## Result

Created a checked publication artifact layer. Four figure candidates are currently drawable only as partial figures; seven remain blocked because the required processed series are missing or incomplete.

## Current Stop Condition

Completion beyond this bounded artifact layer requires processed inputs for the legal-rate timeline, CGA counts, employee and employer contribution comparisons, public-worker reallocation, bank PV sensitivity and combined-balance series. The readiness gate keeps those artifacts blocked or partial until the missing series are registered.

## Validation

This branch ran repository validation and full quality checks after regenerating `MANIFEST.sha256`.
