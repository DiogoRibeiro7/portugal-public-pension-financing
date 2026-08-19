# Build the accounting ontology and concept registry

## Objective
Prevent semantic drift between CGA, RGSS, the previdential system, Social Security as an institution, general government, State Budget transfers and national-accounts concepts.

## Tasks
- Build a machine-readable glossary of every recurring institutional, legal, accounting and actuarial term.
- For each concept record its source definition, valid period and known changes over time.
- Explicitly distinguish institutional accounts from consolidated general-government accounts.
- Define sign conventions for revenue, expenditure, transfers, assets, liabilities and financing residuals.
- Map Portuguese source labels to stable internal variable names without erasing the original labels.

## Outputs
Create `evidence/concept_registry.csv` and `docs/accounting_ontology.md`.

## Acceptance criteria
Every processed dataset must reference valid concept IDs for material flow categories. Ambiguous labels such as `transfer`, `contribution`, `deficit` or `Social Security balance` must not appear without a defined perimeter.
