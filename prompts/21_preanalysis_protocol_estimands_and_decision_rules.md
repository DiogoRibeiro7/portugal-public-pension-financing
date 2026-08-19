# Freeze the pre-analysis protocol, estimands and decision rules

## Objective
Create a formal pre-analysis protocol before confirmatory quantitative work proceeds.

## Tasks
- Inventory every research question and map it to a measurable estimand.
- Separate exploratory reconstruction from confirmatory tests.
- For each hypothesis define the numerator, denominator, population, institutional perimeter, accounting basis, time horizon and tolerance used to judge reconciliation.
- Define what counts as material for remittance gaps, employer gaps and annual residuals using both absolute EUR and scale-relative thresholds.
- Define all alternative combined-balance perimeters before inspecting their final results.
- Define which counterfactuals are legal replications and which are economic scenarios.
- Freeze the protocol with a SHA-256 hash and protocol version.

## Outputs
Create `evidence/analysis_protocol.csv` and `docs/preanalysis_protocol.md`.

Required columns should include hypothesis_id, estimand_id, formula, population, period, unit, accounting_basis, perimeter, primary_sources, tolerance_rule, falsification_rule, exploratory_or_confirmatory and protocol_version.

## Acceptance criteria
No confirmatory notebook may run when its estimand lacks a preregistered definition or required source class.
