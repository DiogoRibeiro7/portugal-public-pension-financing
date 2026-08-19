# Reconstruct the FEFSS capitalization counterfactual

## Objective
Test the claim that post-2006 public-worker contributions would have accumulated to a large share of FEFSS if invested at FEFSS returns.

## Tasks
- Build an official annual FEFSS return series, clearly identifying gross/net return and valuation basis.
- Reproduce the published capitalization convention exactly if documented.
- Test timing assumptions: beginning-of-year, mid-year and end-of-year contribution investment.
- Distinguish actual FEFSS assets from the hypothetical reserve.
- Report nominal and, separately, real values when appropriate.
- Compare the counterfactual with an alternative low-risk government-financing benchmark without selecting the result that favors one interpretation.

## Outputs
Create `data/processed/fefss_returns.csv`, `data/processed/public_worker_fefss_counterfactual.csv` and sensitivity tables.

## Acceptance criteria
The counterfactual must explicitly state that it requires additional retained resources unless an offsetting financing assumption is specified.
