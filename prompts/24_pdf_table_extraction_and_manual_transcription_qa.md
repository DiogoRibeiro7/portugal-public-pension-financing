# Implement PDF/table extraction and transcription quality assurance

## Objective
Make historical extraction auditable when official accounts are published only as PDFs, scans or poorly structured tables.

## Tasks
- Prefer embedded text/table extraction when available.
- For scanned or irregular tables, use controlled manual transcription or a single extraction pass followed by human-style validation; never rely on unchecked OCR output.
- Store page number, table title, row label, column label, original string, parsed numeric value and unit.
- Double-check totals against document subtotals and accounting identities.
- Require a second independent transcription/check for high-impact values used in headline claims.
- Preserve extraction logs and parsing warnings.

## Outputs
Create reusable extraction helpers plus `evidence/extraction_audit.csv`.

## Acceptance criteria
No headline value extracted from a difficult PDF may enter processed data without a page/table locator and a documented validation check.
