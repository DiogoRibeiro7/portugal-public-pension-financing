# Unit Normalization

Status: `partial_bounded_reconstruction`

Registry: `evidence/unit_registry.csv`

Utilities: `src/portugal_pensions/units.py`

## Rules

Nominal EUR in current prices remains the canonical accounting representation
unless a registered real series is explicitly added. Escudo values require the
official fixed conversion rate of 200.482 escudos per euro before any euro join.

Joins across sources must carry compatible metadata:

- unit;
- currency;
- price basis;
- accounting basis;
- flow or stock classification;
- time reference.

The utility `assert_compatible_for_join` fails when those fields differ. The
caller must either convert explicitly or keep the series separate.

## Current Gate

`validate-evidence` now checks that `evidence/unit_registry.csv` has the required
metadata columns, includes every unit token currently observed in evidence and
processed CSVs, and records the fixed escudo/euro conversion rule.

This is a bounded gate. It does not create real-price variants because no price
index has been registered yet.
