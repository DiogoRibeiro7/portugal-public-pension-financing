# Legal contribution history

Status: `partial_bounded_reconstruction`

This note documents `evidence/legal_contribution_registry.csv`.

## Scope

The registry reconstructs a bounded CGA contribution regime from 2006 onward for:

- central state integrated services that were not in the earlier employer-contribution cohorts;
- entities already obliged to contribute before 2007;
- autonomous entities first covered in 2007;
- entities first covered by the broadened 2009 rule.

The perimeter follows Lei n.º 60/2005: from 1 January 2006 CGA stopped accepting new subscribers and new entrants moved to the general Social Security regime. The table therefore applies to workers who remained in the convergent public-sector protection regime.

## Evidence

The current rule is recorded from the consolidated Estatuto da Aposentação, article 6-A. The historical rate path is recorded from official Tribunal Constitucional decisions that quote the budget-law provisions and rate splits. Those decisions identify the relevant statutory articles for 2006, 2007, 2008, 2009, 2010, 2013 and 2014.

## Limitation

The registry is not a complete 1977-2025 rate history. Older budget-law PDFs still need direct article-level extraction and hashing before the table can be treated as fully replicated from primary legislation. Until then, rows marked `verified_official_judicial_summary` should be cited as an official legal reconstruction, not as independently extracted statutory text.

## Validation

`python -m portugal_pensions.cli validate-evidence` now checks duplicate interval keys, rate-component totals, required fields, source IDs, controlled statuses, covered-risk labels, required employer classes, one open interval per employer class, interval direction and overlapping date intervals by employer class.
