# Post-2006 public-worker reallocation

Status: `partial_bounded_reconstruction`

This note documents:

- `data/processed/public_worker_rgss_cohorts.csv`
- `data/processed/public_worker_rgss_contributions_2006_2025.csv`
- `data/processed/public_worker_reallocation_bridge.csv`

## Established Mechanism

Lei n.º 60/2005 closed CGA to new subscribers from 1 January 2006. The mechanical reallocation to be estimated is therefore the worker and employer contribution flow associated with public-sector entrants who would previously have entered CGA but instead entered RGSS.

## Required Inputs

The current registered evidence does not yet provide:

- public-worker new-entrant cohort counts by year and perimeter;
- contribution bases or payroll for those cohorts;
- applicable RGSS contribution rates and pension-risk decomposition by period;
- adjustments separating mechanical reallocation from wage growth, demographic change and general labour-market effects.

## Current Output

The processed files contain year-level records from 2006 through 2025 with blank quantitative fields and `blocked_missing_public_employment_payroll` status.

`public_worker_rgss_contributions_2006_2025.csv` includes method, pension-basis, uncertainty, aggregate-cap and claim-permission fields. These fields prevent a future estimate from entering the analysis unless it is labelled as either a direct observation or a reconstruction and checked against aggregate RGSS contribution revenue.

`public_worker_reallocation_bridge.csv` records the mechanical flow identity:

`contribution_base * worker_rate + contribution_base * employer_rate = total_contributions`

It also records that demographic change, wage growth and general labour-market effects are excluded from this mechanical channel. No contribution-flow amount is estimated yet because the cohort counts, payroll base and applicable RGSS worker and employer rates have not all been extracted from registered primary or official sources.

## Validation

`python -m portugal_pensions.cli validate-evidence` checks that the cohort and contribution files cover every year from 2006 to 2025, reject duplicate year keys, and require non-negative numeric values whenever bounds are populated.

The bridge validation additionally requires:

- one mechanical reallocation row for every year from 2006 through 2025;
- explicit source identifiers, unit, price basis and accounting basis metadata;
- `claim_permitted=no` while rows remain blocked by missing source inputs;
- non-negative numeric values and a zero residual against the flow identity whenever a row is marked complete.
