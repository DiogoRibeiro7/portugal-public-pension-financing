# Discover historical sources and build a coverage-gap map

## Objective
Determine what can actually be reconstructed from 1977-2025 before forcing a continuous series.

## Tasks
- Search official archives for CGA reports, Conta Geral do Estado, budget documents, Social Security accounts, public-employment statistics and legal material.
- Record first/last available year, format, granularity, revisions and whether tables are directly machine-readable.
- Identify years in which definitions or publication formats changed.
- Search archived official catalogues when modern portals expose only recent years.
- Build a gap matrix by variable and year.
- Do not use secondary estimates merely to fill primary-source gaps; register them separately as possible cross-checks.

## Outputs
Create `evidence/source_coverage_matrix.csv` and `docs/historical_data_gap_map.md`.

## Acceptance criteria
The target 1977-2025 horizon must be represented as observed, unavailable, definition-break, revision-conflict or not-applicable for every core variable.
