# Post-2006 public-worker reallocation

Status: `blocked_missing_public_employment_payroll`

This note documents:

- `data/processed/public_worker_rgss_cohorts.csv`
- `data/processed/public_worker_rgss_contributions_2006_2025.csv`

## Established Mechanism

Lei n.º 60/2005 closed CGA to new subscribers from 1 January 2006. The mechanical reallocation to be estimated is therefore the worker and employer contribution flow associated with public-sector entrants who would previously have entered CGA but instead entered RGSS.

## Required Inputs

The current registered evidence does not yet provide:

- public-worker new-entrant cohort counts by year and perimeter;
- contribution bases or payroll for those cohorts;
- applicable RGSS contribution rates and pension-risk decomposition by period;
- adjustments separating mechanical reallocation from wage growth, demographic change and general labour-market effects.

## Current Output

The two processed files contain year-level records from 2006 through 2025 with blank quantitative fields and `blocked_missing_public_employment_payroll` status. No contribution-flow amount is estimated yet.

## Validation

`python -m portugal_pensions.cli validate-evidence` checks that the cohort and contribution files cover every year from 2006 to 2025, reject duplicate year keys, and require non-negative numeric values whenever bounds are populated.
