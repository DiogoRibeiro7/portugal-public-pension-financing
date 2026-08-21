# Public Sector Perimeter And Employer Classes

Status: `partial_bounded_reconstruction`

This note documents `evidence/employer_perimeter_registry.csv`. The registry is
a join guard: employer-liability reconstruction must join legal rates by
employer class and effective date, not by a broad public-sector label or by
national-accounts sector alone.

## Current Mapping

The bounded registry identifies four CGA retained-subscriber employer classes
that correspond to the legal-rate registry:

- `central_state_integrated_services`;
- `entities_already_contributing_before_2007`;
- `autonomous_entities_first_covered_2007`;
- `entities_first_covered_2009`.

It also records `public_workers_rgss_new_entrants_2006` as a boundary row. New
public-sector entrants from 2006 belong to RGSS rather than to the retained CGA
subscriber legal-rate table.

## Separation Rule

The fields `legal_regime`, `statistical_sector`, and
`national_accounts_sector` must remain distinct. A public institute, autonomous
service, university, public enterprise, or other employer can require a legal
contribution class that does not map one-to-one to a national-accounts sector.
Rows therefore keep legal class, statistical description, and ESA/general
government classification separate until entity-year sources are acquired.

## Validation

`validate_employer_perimeter_registry` checks required employer classes, legal
class crosswalks, source IDs, controlled statuses, RGSS entrant-rule labels,
duplicate keys, interval direction, and overlapping intervals. It also rejects
rows that collapse the legal regime and statistical sector into the same field.

## Limitation

This is not a complete entity-year public-employer panel. DGAEP, CGA, CGE,
budget-law and national-accounts sources still need to be acquired and joined at
entity-year level before employer payroll bases or recorded contributions can be
allocated across restructurings, mergers, privatizations, or ESA
reclassifications.
