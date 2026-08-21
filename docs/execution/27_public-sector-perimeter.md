# Map public sector perimeter

Instruction file: `prompts/27_public_sector_perimeter_and_employer_class_mapping.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Added employer perimeter rows for the four CGA retained-subscriber legal-rate classes and the post-2006 RGSS entrant boundary.
- Added a date-based employer-class lookup utility.
- Added validation for legal-class crosswalks, source IDs, controlled statuses, RGSS entrant-rule labels, duplicate keys, interval direction, overlaps and legal/statistical-sector separation.
- Preserved existing validated outputs and did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added an executable bounded public-sector perimeter gate. The registry prevents employer-liability reconstruction from applying one legal rate to entities subject to different contribution regimes in the same year.

## Current Stop Condition

Completion beyond this record requires entity-year public-employer classification, payroll-base and reclassification sources from DGAEP, CGA, CGE, budget-law and national-accounts materials. Until then, the mapping is a legal-class guard rather than a complete employer panel.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
