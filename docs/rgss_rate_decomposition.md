# RGSS Rate Decomposition

Status: `partial_bounded_reconstruction`

The executable registry is `evidence/rgss_rate_decomposition.csv`. It separates
the full RGSS contribution rate from a narrower pension-risk benchmark and from
unmapped non-pension risks.

## Current Bounded Result

The current source set supports one bounded 2012 comparison from the Tribunal de
Contas Social Security budget-execution report:

- Full RGSS broad social-protection rate: 34.75 percent.
- Comparable covered-eventuality benchmark: 26.94 percent of payroll.
- Residual non-pension-risk component: 7.81 percentage points.

The covered-eventuality benchmark is labeled as an economic counterfactual, not
as a historical CGA legal obligation or legal debt. The full RGSS rate remains
available only as a broad social-protection scenario and must not be described as
pension-only.

## Guardrails

- A CGA legal-rate comparison must use the actual legal contribution registry.
- A pension-risk comparison must carry the `economic_counterfactual` label.
- Non-pension RGSS risks cannot be assigned to public employers until direct
  sickness, unemployment, parental, death, and other employer-borne risk sources
  are mapped.
- The historical RGSS decomposition remains incomplete until year-level legal and
  Social Security account sources are extracted.

## Remaining Gaps

- Legal RGSS rates by period and contingency are not yet reconstructed for
  1977-2025.
- The allocation of full RGSS rates between worker and employer by contingency
  remains unavailable in the machine-readable evidence layer.
- Directly borne public-employer risks outside CGA remain unmapped.
