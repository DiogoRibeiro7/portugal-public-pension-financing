# Build FEFSS return engine

Instruction file: `prompts/35_fefss_return_series_and_capitalization_engine.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Preserved existing validated outputs.
- Added a deterministic capitalization function with beginning-, mid- and end-year timing conventions.
- Replaced header-only FEFSS files with blocked, source-registered rows and validation for annual return conventions and capitalization companions.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded FEFSS return and capitalization gate. The engine is deterministic, but all FEFSS return values and public-worker capitalization outputs remain blocked until official annual return measures, valuation basis, fees basis and contribution cash flows are extracted.

## Current Stop Condition

Completion beyond this gate requires official annual FEFSS return data with return type, valuation basis, fees treatment, source/page provenance and explicit contribution-timing convention. Until those inputs exist, the repository must not use FEFSS returns in a manuscript claim.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
