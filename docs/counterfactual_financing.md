# Counterfactual Financing Regimes

`data/processed/counterfactual_financing_regimes.csv` implements the preregistered scenarios in `evidence/counterfactual_registry.csv` as a rule table.

The table is deliberately not a numerical scenario result table. Current registered sources do not yet provide all payroll bases, contribution receipts, annual State transfers, FEFSS returns, bank pension cash-flow schedules, investment income or asset drawdown paths needed for complete counterfactual histories.

## Stock-Flow Rules

- `CF1` preserves realised pension payments and treats legal-remittance changes as requiring an explicit State-transfer adjustment.
- `CF2` uses `funding_substitution` so alternative employer financing reduces State Budget transfers one-for-one and does not create extra cash.
- `CF3` uses `compound_reserve`, but reserve contributions must be booked as additional historical expenditure unless another financing source is explicitly reduced.
- `CF4` requires the full bank pension stream: transferred assets, investment income, State financing and pension expenditure. Asset exhaustion dates alone are not an accepted comparison.

Rows with blocked statuses mark missing evidence inputs and must not be interpreted as zero-valued results.
