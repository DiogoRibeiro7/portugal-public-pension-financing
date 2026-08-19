# Resolve source conflicts, revisions and uncertainty

## Objective
Define what to do when two official sources report different values for the same apparent quantity.

## Tasks
- Never overwrite one source with another.
- Classify differences as revision, perimeter, timing, accounting basis, transcription, rounding or unresolved.
- Prefer final audited accounts for institutional cash values, but preserve national-accounts values when the estimand is an ESA balance.
- Define reconciliation tolerances by scale and source type.
- Assign uncertainty/confidence labels to reconstructed historical values.
- Propagate unresolved ranges into derived results where material.

## Outputs
Create `evidence/source_conflict_registry.csv` and `evidence/uncertainty_registry.csv`.

## Acceptance criteria
Every material disagreement must end in either a documented reconciliation or an explicit unresolved range; never select the value that better supports the provisional thesis.
