# Extraction QA

Status: `partial_bounded_reconstruction`

Audit table: `evidence/extraction_audit.csv`

Reusable helpers: `src/portugal_pensions/extraction.py`

## Rule

Every extracted value used by processed data must carry:

- source ID;
- page or official-page locator;
- table title;
- row and column labels;
- original source string;
- parsed value and unit;
- extraction method;
- validation method;
- QA tier;
- secondary-check status;
- parsing-warning status.

Rows marked `high_impact` require a documented secondary check. Rows that rely
on OCR cannot be accepted if the validation method says the OCR was unchecked.

## Current Gate

`validate-evidence` now validates the extraction audit. It checks required
columns, source IDs, duplicate locators, numeric parsed values, high-impact
secondary checks, parsing warnings, and two existing accounting consistency
checks:

- CGA 2011 balance excluding the PT fund reconciles to the reported CGA and PT
  fund values within rounding tolerance.
- The 2012 banking substitute-regime revenue and expenditure extractions match.

This is a bounded gate. It does not claim that all source tables have been
extracted; it prevents current and future extracted headline values from
entering the repository without locators and documented checks.
