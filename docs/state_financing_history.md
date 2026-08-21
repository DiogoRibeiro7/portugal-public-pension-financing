# State Financing History

Status: `partial_bounded_reconstruction`

This note records the current evidence-bounded State-financing reconstruction. The
machine-readable rule inventory is `evidence/state_financing_rule_registry.csv`.

## Current Rule Categories

- `budget_appropriation_route`: the DGO State Budget archive is registered as the
  route for annual reports, proposals, laws, and maps from 1996 onward. This is a
  source route, not a completed annual transfer series.
- `accounting_presentation_rule`: the Tribunal de Contas 2013 Social Security
  budget-execution report presents CGA financing sources separately from uses of
  funds for 2012.
- `specific_state_transfer`: Decree-Law 127/2011 and the 2012 Social Security
  execution account identify a specific State transfer for assumed bank-pension
  responsibilities. This must remain separate from ordinary subsystem financing.
- `transferred_asset_financing`: the 2011 State account and the bank-pension legal
  framework record transferred pension-fund assets as a financing or liquidity
  resource. This is not a current employer contribution.

## Classification Rules

Employer contributions, balancing transfers, extraordinary/specific transfers,
and asset receipts are distinct financing mechanisms. A recorded transfer is not,
by itself, evidence of underfunding, a deficit, or legal noncompliance. Each annual
amount must first be classified by legal basis, accounting basis, recipient, and
settlement rule.

The current registry therefore records rule categories and guardrails rather than
claiming a complete historical series. Annual values can only be interpreted after
the corresponding State Budget, State account, CGA account, and Social Security
account tables are extracted and reconciled.

## Remaining Gaps

- Annual State Budget appropriations and settlement rules have not yet been
  extracted into a complete 1977-2025 series.
- CGA annual accounts are still required to separate employer contributions,
  State transfers, other public transfers, and residual financing consistently.
- Post-2012 special-transfer execution for assumed banking responsibilities
  remains incomplete.
- The DGO archive route must be converted into year-level source records before
  fixed, residual, appropriated, or settled transfer formulas can be assigned.
