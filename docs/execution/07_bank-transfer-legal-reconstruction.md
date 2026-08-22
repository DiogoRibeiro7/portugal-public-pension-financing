# Reconstruct bank transfer law

Instruction file: `prompts/07_bank_transfer_legal_reconstruction.md`
Date: 2026-08-22
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Added `data/processed/bank_transfer_legal_coverage.csv` to tie the four required legal instruments and DL127 extraction requirements back to registry record IDs.
- Added validation for required timeline instruments, DL127 required fields, referenced registry rows, status values, and the unresolved raw-PDF limitation for DL127.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Recorded a validated legal-coverage gate for the bank-transfer reconstruction. The registry contains the article-level DL127 design facts and the 18 listed institutions, while unresolved monetary schedules remain blocked.

## Current Stop Condition

Completion beyond this bounded legal reconstruction requires a reliable raw PDF endpoint for DL127 plus bank-level valuation schedules, transferred-asset composition, independent valuer identity, and final adjustment records. Until those inputs exist, economic net-benefit claims remain blocked.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
