# Add unit normalization

Instruction file: `prompts/25_units_currency_price_basis_and_time_alignment.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Expanded `evidence/unit_registry.csv` to cover all unit tokens currently used
  in evidence and processed CSVs.
- Added `src/portugal_pensions/units.py` with fixed escudo/euro conversion,
  unit-registry loading, canonicalization, and join-compatibility checks.
- Added a unit-registry validation gate to `validate-evidence`.
- Replaced the placeholder unit-normalization note with the current executable
  rule.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded unit/currency/price-basis/time-alignment gate.

## Current Stop Condition

Completion beyond this record requires registering any future price index before
building real-price variants and adding explicit conversion rows before joining
new source units. The current gate covers the repository's current nominal and
ratio units only.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` and `make quality`
after regenerating `MANIFEST.sha256`.
