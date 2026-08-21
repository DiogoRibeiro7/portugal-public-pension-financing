# Acquire and hash sources

Instruction file: `prompts/01_source_acquisition_and_hashing.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Attempted all 16 registered official sources without raw files.
- Acquired and hashed 8 usable source pages under `data/raw/source_catalogues/`.
- Recorded 5 Diario da Republica shell-HTML captures as not usable evidence.
- Recorded 3 failed acquisition attempts for later source work.
- Added `evidence/source_acquisition_log.csv` and `docs/source_acquisition.md`.
- Added an acquisition-log validation gate tying raw files to the source
  registry and SHA-256 hashes.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded raw-source acquisition and hashing pass for reachable registered
official sources.

## Current Stop Condition

Completion beyond this record requires acquiring the remaining official sources,
especially the DGO archive routes, the Banco de Portugal ESA2010 page, and
Diario da Republica full-text/PDF forms that are not shell HTML. The current
pass does not extract historical tables or fill quantitative gaps.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` and `make quality`
after regenerating `MANIFEST.sha256`.
