# Normalize units, currency, price basis and time alignment

## Objective
Prevent false historical comparisons caused by escudos/euros, thousands/millions, nominal/real values, calendar timing or cash/accrual differences.

## Tasks
- Preserve source currency and unit before conversion.
- Apply the official fixed escudo/euro conversion only where appropriate and record the conversion rule.
- Keep nominal EUR as the canonical accounting representation unless a real series is explicitly requested.
- Build deflated variants only with a registered price index and base year.
- Distinguish flow year, payment year, accounting year and valuation date.
- Record whether a source is cash, accrual, budget execution, financial accounting or ESA national accounts.

## Outputs
Create `evidence/unit_registry.csv`, normalized conversion utilities and validation tests.

## Acceptance criteria
All joins across sources must fail when unit, currency or accounting-basis metadata are incompatible and no explicit conversion exists.
