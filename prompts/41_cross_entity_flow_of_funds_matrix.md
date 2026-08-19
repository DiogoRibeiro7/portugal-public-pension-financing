# Build a cross-entity stock-flow-consistent pension financing matrix

## Objective
Prevent double counting by representing who pays whom across the entire system.

## Entities
At minimum distinguish households/workers, public employers, private banks, private pension funds, CGA, Social Security, FEFSS, State Budget/Treasury and consolidated general government.

## Tasks
- Build annual transaction matrices for contributions, pension payments, State transfers, asset transfers and internal public flows.
- Enforce row/column consistency where the same transaction is observed on both sides.
- Mark transactions that disappear under general-government consolidation.
- Separate stocks (assets/liabilities) from flows (contributions/transfers/expenditure).
- Create bridge tables from institutional balances to consolidated balances.

## Outputs
Create `data/processed/pension_flow_of_funds_long.csv` and reconciliation tests.

## Acceptance criteria
Every combined-balance calculation must be derivable from an explicit selection of rows in the flow-of-funds matrix.
