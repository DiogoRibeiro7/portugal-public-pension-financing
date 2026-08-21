# Build source coverage map

Instruction file: `prompts/23_historical_source_discovery_and_gap_map.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Ran a bounded official-source discovery pass across DGO, CGA, IGFSS/Social
  Security, DGAEP, Diario da Republica, INE, Banco de Portugal, and Tribunal de
  Contas routes.
- Registered official catalogue anchors in `evidence/source_registry.csv`
  without marking undownloaded files as acquired.
- Rebuilt `evidence/source_coverage_matrix.csv` as a complete 1977-2025 grid
  for 12 core variables.
- Added `docs/historical_data_gap_map.md` documenting observed anchors,
  unavailable gaps, definition breaks, revision conflicts, and the rule against
  filling primary-source gaps with secondary estimates.
- Added a validation gate for the coverage matrix and gap-map documentation.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded historical source coverage matrix. The matrix represents the
1977-2025 horizon for core public-account, CGA, Social Security,
public-employment, legal, bank-transfer, and ESA accounting variables.

## Current Stop Condition

Completion beyond this record requires downloading, hashing, and extracting the
year-level files behind each catalogue route, plus archived searches for
pre-modern portal gaps. Until then, rows marked `observed` mean source route
identified, not table extracted.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` and `make quality`
after regenerating `MANIFEST.sha256`.
