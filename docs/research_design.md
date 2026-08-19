# Research design

## 1. Scientific objective

The project reconstructs the financing architecture of Portuguese public pensions before evaluating modern claims about CGA and Social Security balances.

The main empirical object is not a single balance. It is a linked system of legal obligations, cash flows, transferred assets, pension payments and public-budget transfers.

## 2. Four analytical lenses

### Legal lens

What was each worker and employer legally required to contribute in each period?

### Cash-accounting lens

What was actually recorded as withheld, received, transferred and paid?

### Consolidated-public-finance lens

Which flows are internal transfers within general government and which cross the government boundary?

### Intertemporal/actuarial lens

What pension liabilities were created or transferred, with which valuation assumptions and which assets?

## 3. Non-equivalence rules

The following quantities must never be treated as synonyms:

```text
legal contribution shortfall != economic benchmark gap
institutional deficit != consolidated fiscal cost
cash transfer != actuarial liability
asset transfer != income without a corresponding obligation
RGSS employer rate != pension-only employer rate
unexplained residual != diversion of funds
```

## 4. Main hypotheses

See `paper/hypotheses.md` for the preregistered hypotheses and failure conditions.

## 5. Banking-sector transfer module

The 2011 transaction is analysed as a transfer of both assets and obligations.

The legal design is unusual enough to require a dedicated ledger:

```text
bank pension fund assets -> State
specified pensions in payment -> Social Security responsibility
State -> specific financing transfer -> Social Security
Social Security -> pension payment process
covered bank responsibilities -> extinguished
remaining updates/complements/etc. -> bank pension funds
```

The research must separately test:

1. whether the actuarial value of assets matched liabilities under the statutory 4% discount-rate assumptions at inception;
2. sensitivity of that equality to alternative discount rates and mortality assumptions;
3. whether the State actually funded annual pension payments as prescribed;
4. whether Social Security experienced uncompensated cash or administrative costs;
5. how the operation affected the 2011 headline deficit under ESA-95;
6. how the same operation is treated under ESA-2010;
7. the long-run cumulative cost of the transferred pensions;
8. the economic relief obtained by participating banks from extinguished liabilities;
9. the effect of bank-worker contributions entering the general regime after integration.

## 6. Historical CGA module

For CGA, the project first reconstructs the legal contribution regime by employer class and year. A modern contribution rate must never be projected backward unless used explicitly as a counterfactual benchmark.

## 7. Falsification-first rule

Before manuscript drafting, every substantive hypothesis must have an explicit condition under which it is rejected or weakened.
