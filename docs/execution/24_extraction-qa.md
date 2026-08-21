# Add extraction QA

Instruction file: `prompts/24_pdf_table_extraction_and_manual_transcription_qa.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Added reusable extraction helpers in `src/portugal_pensions/extraction.py`.
- Expanded `evidence/extraction_audit.csv` with QA tier, secondary-check, and
  parsing-warning fields.
- Marked high-impact extracted values that require a documented second check.
- Added an extraction-audit validation gate covering source IDs, locators,
  parsing, high-impact checks, unchecked OCR, duplicate rows, and existing
  accounting consistency checks.
- Replaced the placeholder extraction QA documentation with the executable rule.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded extraction QA gate around current audit rows and reusable
helpers for future extraction records.

## Current Stop Condition

Completion beyond this record requires acquiring and extracting the remaining
year-level official tables. The current gate validates extraction provenance
for rows already present; it does not complete all historical extraction.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` and `make quality`
after regenerating `MANIFEST.sha256`.
