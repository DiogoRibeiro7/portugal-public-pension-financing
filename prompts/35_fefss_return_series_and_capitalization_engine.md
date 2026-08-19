# Build the official FEFSS return series and capitalization engine

## Objective
Create the validated return series and deterministic capitalization mechanics needed by the post-2006 public-worker counterfactual.

## Tasks
- Acquire official FEFSS annual reports and identify annual return measures, fees and valuation conventions.
- Preserve reported return type and do not mix gross, net, nominal or real returns.
- Build a clean annual series with source/page provenance.
- Implement deterministic capitalization for arbitrary annual cash flows under beginning-, mid- and end-year timing assumptions.
- Add tests for compounding identities, missing years and sign conventions.
- Export companion CSVs for every capitalization result.

## Outputs
Create `data/processed/fefss_returns.csv` and reusable capitalization functions under `src/portugal_pensions/`.

## Acceptance criteria
Any manuscript claim using FEFSS returns must be reproducible from the official return series and an explicit contribution-timing convention.
