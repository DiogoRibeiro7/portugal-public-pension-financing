# Falsification Report

This report records adversarial tests that must be passed before the manuscript can state stronger conclusions. It is backed by `data/processed/falsification_review.csv`.
The claim-language boundary is enforced in `evidence/falsification_decision_requirements.csv`.

## Current Result

The review does not overturn any registered result that is currently supported by evidence, but most challenges remain unresolved because the necessary primary-source inputs are missing. Those unresolved tests are blockers on strong causal or lifecycle-cost language.

## Test Outcomes

| Test | Challenge | Current decision |
| --- | --- | --- |
| FALS_001 | Employee remittance gaps are timing artefacts | Unresolved: payroll withholding, CGA quota revenue and timing adjustments are missing. |
| FALS_002 | Employer gaps come from incorrect legal rates | Bounded: legal-rate confusion is guarded, but payroll and recorded-revenue values are missing. |
| FALS_003 | State transfers were intended historical financing | Unresolved: transfer-purpose components and legal classification remain incomplete. |
| FALS_004 | The 2006 RGSS effect is smaller than claimed | Unresolved: public-worker cohorts, contribution bases and rates are missing. |
| FALS_005 | Combined deficits depend on perimeter choices | Unresolved numerically: the flow-of-funds matrix guards perimeter selection, but RGSS and FEFSS annual flows are missing. |
| FALS_006 | The 2011 bank transfer was balanced once specific State financing is included | Partially reconciled: 2012 financing and pension payments both equal EUR 516.0m in the official audit, but lifecycle costs remain unresolved. |
| FALS_007 | The bank transfer appears adverse only under selectively chosen discount rates | Unresolved: the 2 to 6 percent sensitivity grid cannot be populated without pension cash-flow and demographic schedules. |
| FALS_008 | The bank transfer remains adverse under conservative assumptions and full legal financing | Unresolved: full pension cash flows, asset composition, asset income, State financing and retained bank liabilities are missing. |

## Manuscript Gate

Until the blocked inputs are acquired, the manuscript may state only bounded findings: source-backed legal mechanisms, extracted account values, reconciliation identities and explicit data gaps. It must not claim a definitive remittance loss, employer underpayment amount, combined-balance sign, bank-transfer subsidy or lifecycle public-finance loss.
The decision gate keeps each unresolved challenge tied to its blocked language so later manuscript edits cannot convert missing-input limitations into final conclusions.
