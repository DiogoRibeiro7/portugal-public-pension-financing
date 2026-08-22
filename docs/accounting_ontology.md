# Accounting Ontology

Status: `partial_bounded_reconstruction`

The machine-readable ontology is `evidence/concept_registry.csv`. It is a
controlled glossary and crosswalk for recurring institutional, legal,
accounting, national-accounts, and actuarial terms used by the current bounded
research artifacts.

## Scope

The registry distinguishes these perimeters before any balance or financing
claim is allowed:

- CGA institutional accounts.
- RGSS institutional accounts.
- The Social Security previdential subsystem.
- Competing combined-balance perimeters are recorded in
  `data/processed/joint_balance_definitions.csv`; each row names the applicable
  inclusion, exclusion, consolidation, historical-adjustment, and bank-special
  sensitivity rules before any numerical series is accepted.
- Special bank-pension transfer ledgers.
- Consolidated general-government and ESA national-accounts measures.

The registry also separates cash/accounting flows from legal obligations,
stock valuations, actuarial present values, and reconciliation residuals.

## Sign Conventions

Material concepts use explicit signs in `sign_convention`:

- Revenues and financing inflows are positive to the receiving institution.
- Pension and administration expenditure are negative for balance identities.
- Asset transfers are positive when received by the public-sector ledger.
- Pension liabilities are positive stock obligations.
- Residuals and timing adjustments are signed reconciliation diagnostics.
- ESA deficit effects use a separate national-accounts sign rule.

No table may rely on an unlabeled `transfer`, `contribution`, `deficit`,
`liability`, or `balance` without a concept row that states perimeter,
accounting basis, and guardrail language.

## Current Gate

`validate-evidence` checks that:

- `evidence/concept_registry.csv` has the required ontology columns.
- Required concept IDs are present.
- Source-defined concepts reference known source IDs.
- Material columns in the core processed ledgers map to concept IDs.
- Registry mappings point to existing datasets and existing columns.

This gate is deliberately bounded. It enforces semantic consistency for the
current processed files, but it does not certify that every historical source
definition has been acquired or that all future datasets are complete.
