# Define actuarial identifiability and defensible bounds for the bank transfer

## Objective
Prevent false precision when revaluing transferred bank-pension liabilities without beneficiary-level cash flows.

## Tasks
- Inventory available data on pensioner age, sex, pension amount, survivor status, mortality table, indexation and expected cash-flow duration.
- Determine which alternative actuarial valuations are point-identified, partially identified or not identifiable.
- Reproduce the statutory valuation assumptions exactly where possible.
- If individual or cohort cash flows are unavailable, build transparent bounds/sensitivity envelopes rather than synthetic microdata presented as fact.
- Separate discount-rate sensitivity from longevity sensitivity and indexation sensitivity.

## Outputs
Create `evidence/actuarial_identifiability_registry.csv` and validated sensitivity functions.

## Acceptance criteria
No alternative present value may be reported with more precision than the underlying public data support.
