# Build accounting ontology

Instruction file: `prompts/22_accounting_ontology_and_concept_registry.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Expanded `evidence/concept_registry.csv` into a machine-readable ontology with
  source-definition status, sign conventions, stable variable names, and
  material-column mappings.
- Added an executable concept-registry gate to `validate-evidence`.
- Replaced the placeholder ontology note with the current bounded accounting
  ontology rules.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added a bounded accounting ontology gate that prevents material ledger columns
from drifting away from explicit concept IDs, perimeters, accounting bases, and
sign conventions.

## Current Stop Condition

Completion beyond this record requires source-complete historical definitions
and deterministic extraction records for all institutional and national-accounts
labels. Until those inputs exist, the ontology remains a bounded consistency
gate rather than a complete historical thesaurus.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` and `make quality`
after regenerating `MANIFEST.sha256`.
