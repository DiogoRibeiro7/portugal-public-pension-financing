# Source Conflict And Uncertainty Policy

Status: `partial_bounded_reconstruction`

This policy defines how conflicting official values are recorded while the
repository remains a bounded research snapshot. It does not authorize selecting
the value that best supports a thesis, overwriting an earlier official value, or
treating unresolved differences as solved.

## Registries

- `evidence/source_conflict_registry.csv` records source pairs, values, units,
  difference classes, materiality rules, and resolution status.
- `evidence/uncertainty_registry.csv` records the lower, central, and upper
  values that must be carried when a conflict leaves an estimate bounded rather
  than point-identified.

## Difference Classes

- `revision`: later official releases revise an earlier official value.
- `perimeter_and_accounting_item`: values describe different institutions,
  accounts, flows, stocks, or booked items.
- `timing`: values refer to different recognition dates, payment dates, or
  accrual periods.
- `accounting_basis`: values differ because ESA, public-account, legal, or
  institutional cash bases answer different estimands.
- `transcription`: a value is suspected to reflect extraction or transcription
  error and must be traced back to the source image or table.
- `rounding`: values reconcile within the precision published in source tables.
- `rounding_approximation`: a narrative or rounded benchmark reconciles with a
  more precise audited value within an explicit tolerance.
- `unresolved`: available sources do not yet support a deterministic
  reconciliation.

## Preference Rules

Final audited institutional accounts are preferred for institutional cash
expenditure, revenue, and transfer ledgers. ESA values are not overwritten by
institutional cash values when the estimand is an ESA balance, deficit, or
national-accounts treatment. Exact legal amounts are preserved for legal
transfer facts, while rounded account-table values remain as cross-checks.

When two official values are not the same accounting quantity, the repository
keeps both values as separate concepts or estimands. It must not net them, blend
them, or choose one without a documented accounting reason.

## Tolerances

Rounding is acceptable only within the source table scale. Narrative
approximations require an explicit tolerance in the conflict registry. ESA
standard changes are resolved by estimand and accounting standard rather than by
numeric tolerance. Differences above the stated materiality rule remain
unresolved unless the resolution field documents a source-grounded
reconciliation.

## Uncertainty Propagation

Every unresolved range must have a linked `uncertainty_id`. Rows with
`unresolved_range` status carry lower and upper bounds and leave the central
value empty until the missing source or reconciliation is acquired. Downstream
outputs that consume an unresolved estimate must propagate the range instead of
reporting a single central value.

## Current Gate

`validate_conflict_and_uncertainty_registries` checks that conflict rows link to
registered sources, concepts, units, and uncertainty rows; that difference types
and statuses use the controlled vocabulary; that values and bounds are numeric;
and that unresolved ranges do not report a central estimate.
