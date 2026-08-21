# Freeze analysis protocol

Instruction file: `prompts/21_preanalysis_protocol_estimands_and_decision_rules.md`
Date: 2026-08-19
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Checked the current counterfactual registry, combined-balance scaffolding, claim gates, and
  release-readiness gates.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.
- Expanded `evidence/analysis_protocol.csv` to protocol version `0.3.0`.
- Added explicit numerator, denominator, materiality, counterfactual class, alternative perimeter,
  and required source-class fields.
- Added `evidence/analysis_protocol_hash.csv`.
- Added validation and tests for protocol coverage and hash integrity.

## Result

Added a bounded frozen protocol covering the current confirmatory estimands and repository gates.
Most quantitative estimands remain source-blocked, but their definitions and decision rules are now
machine-checkable before final confirmatory work.

## Current Stop Condition

Completion beyond this record requires the registered primary sources and deterministic extraction
chain needed by each `required_source_class`. Until those inputs exist, quantitative results remain
blocked or partial under the repository evidence rules.

## Validation

This branch ran `python -m portugal_pensions.cli validate-all` after regenerating `MANIFEST.sha256`.
