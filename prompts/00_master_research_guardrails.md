# Master research guardrails

You are working inside the existing repository `portugal-public-pension-financing`.

Do not rebuild the repository. Extend the existing architecture, evidence registries, notebooks, package code, tests and manuscript scaffold.

This project studies politically contested historical pension financing. It must be evidence-led rather than conclusion-led.

## Scientific neutrality

Never assume that:

- CGA was deliberately underfunded;
- employee deductions were withheld from CGA;
- State Budget transfers prove a structural pension deficit;
- the current Social Security surplus is artificial;
- CGA and RGSS should always be combined;
- the 2011 banking-sector pension transfer was neutral;
- the 2011 banking-sector pension transfer was harmful;
- transferred bank-pension assets were free fiscal revenue;
- exhaustion of a transferred asset pool proves the original transaction was adverse;
- a lower historical employer contribution than a modern RGSS rate was legally unpaid debt;
- a current cash surplus proves long-run actuarial sustainability;
- a current cash deficit proves historical mismanagement.

The repository must be capable of producing results that contradict the initial suspicions motivating the research.

## Objects that must remain distinct

Never collapse the following into a single variable or interpretation:

1. employee contributions legally due;
2. employee deductions actually withheld;
3. employee contributions recorded as received;
4. employer contributions legally due;
5. employer contributions recorded as received;
6. State Budget transfers;
7. transfers between general-government entities;
8. pension assets transferred from private funds;
9. actuarial pension liabilities;
10. institutional cash balances;
11. national-accounts balances;
12. consolidated general-government cost;
13. legal debt;
14. economic benchmark gap;
15. counterfactual reserve accumulation;
16. accrued future pension rights.

## Evidence hierarchy

Prefer, in order:

1. primary legislation and official legal records;
2. audited or official annual accounts;
3. official statistical/national-accounts releases;
4. Tribunal de Contas and other official audits;
5. official technical evaluations;
6. peer-reviewed academic literature;
7. institutional working papers;
8. media reports only for identifying claims that must then be traced to underlying evidence.

Do not use a newspaper as numerical evidence when a primary source exists.

## Provenance contract

Every material number must preserve:

`source -> raw file -> extraction -> normalized value -> transformation -> result -> table/figure -> manuscript claim`.

Raw sources are immutable. Revised official files must be stored as separate revisions with hashes and retrieval dates.

Never manually edit generated evidence files to make them match a desired result.

## Historical-data policy

- Never silently interpolate historical gaps.
- Never back-project modern legal rates as if they were historical legal obligations.
- Keep nominal and real quantities distinct.
- Preserve original currency and unit metadata before conversion.
- Distinguish cash, accrual, budget, institutional-accounting and ESA national-accounts bases.
- Preserve institutional perimeter changes explicitly.
- If two official sources disagree, retain both values until reconciliation is documented.

## Actuarial policy

Do not create beneficiary-level actuarial precision from aggregate data.

If age, sex, mortality, indexation or cash-flow schedules are unavailable, use reproducible bounds or sensitivity analysis and state what cannot be identified.

A statutory discount rate is a legal valuation assumption, not automatically the economically correct discount rate.

## Counterfactual policy

Every counterfactual must specify:

- changed variable;
- unchanged variables;
- financing source;
- budget identity;
- return/discount assumption;
- legal versus economic status;
- whether it changes only accounting classification or real resources.

A funded reserve requires an explicit financing source. Additional historical contributions cannot simultaneously reduce State transfers and accumulate as an untouched reserve unless the counterfactual explicitly finances both.

## Banking-transfer policy

For the 2009-2012 banking modules, separately track:

- active workers entering RGSS;
- pensions already in payment transferred to Social Security;
- assets transferred to the State;
- responsibilities extinguished for banks;
- responsibilities retained by banks;
- State-specific financing of the transferred pensions;
- treatment under ESA-95 and ESA-2010;
- consolidated public-debt/financing effects.

Do not infer a subsidy from liability transfer alone.

## Software and research engineering

Use transparent deterministic methods. No machine learning is required.

Production Python must be typed, documented and tested. Prefer NumPy/pandas/scipy/matplotlib and avoid unnecessary dependencies.

All important notebook results must be exported to machine-readable files and validated outside notebook state.

## Agent behaviour

When evidence is insufficient, stop the claim rather than filling the gap with plausibility.

When a result conflicts with the provisional thesis, preserve it.

When legal interpretation is uncertain, label it as interpretation and identify the primary text that creates the uncertainty.

When a result changes materially under a reasonable definition, report the sensitivity rather than selecting the preferred definition.
