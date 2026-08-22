# Replicate 2026 working group

Status: `partial_bounded_reconstruction`

This note records the executable replication state for the 2026 Social Security
working-group claims. The complete report package is not registered in the
repository: report text, annexes, methodological notes, released spreadsheets,
and source-table bridges are all still missing.

## Claim Targets

The public claim registry now records the five required targets:

- cumulative post-2006 public-worker RGSS contribution estimate
- FEFSS-style capitalization of post-2006 public-worker contributions
- share of FEFSS represented by the hypothetical capitalization result
- combined CGA and previdential Social Security balance
- 2025 adjusted current-balance deficit after specified corrections

Each target is classified as `blocked_primary_source_missing`. Quantities and
replicated values are intentionally blank. Media coverage can identify that
these claims are public, but it is not sufficient numerical evidence for
replication.

## Replication Boundary

The companion table at `data/processed/working_group_2026_replication.csv`
records the missing input artifacts and the blocked transformation for each
claim. No cash-flow timing, return convention, perimeter bridge, or adjustment
bridge is inferred from headline values.

## Stop Condition

Moving any row to `reproduced`, `approximately_reproduced`, or `not_reproduced`
requires the registered primary report package and deterministic extraction
chain. Until then, the repository can only state that the claim set has been
identified and guarded against unsupported numerical reuse.
