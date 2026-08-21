# Decompose RGSS rates

Instruction file: `prompts/29_rgss_rate_decomposition_and_pension_only_benchmark.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Replaced the passive RGSS-rate header with a validated decomposition registry.
- Added 2012 bounded rows separating full RGSS broad social-protection rate,
  comparable covered-eventuality benchmark, and residual non-pension risks.
- Added benchmark lookup helpers that return legal-status labels with rates.
- Preserved the rule that economic benchmarks are counterfactual and not legal
  debt.

## Result

Added an executable RGSS rate decomposition gate.

## Current Stop Condition

Completion beyond this bounded result requires year-level legal RGSS rate tables
by contingency, worker/employer allocations by contingency, and direct
public-employer risk mapping for non-pension contingencies.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
