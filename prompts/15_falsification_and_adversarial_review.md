# Falsification and adversarial review

## Execution contract

Use this prompt together with `00_master_research_guardrails.md`.

Work inside the existing repository. Do not rebuild the project or bypass the established evidence registries, notebooks, validation code, or provenance chain.

Before implementation:

1. inspect the relevant source code, notebooks, registries, configuration and tests;
2. identify the exact primary-source evidence needed;
3. state any data limitation that prevents the requested analysis;
4. preserve all existing validated outputs unless a documented correction is required.

Do not invent missing historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs. If a required quantity cannot be identified from public evidence, record the limitation and implement a bounded or partial analysis instead of fabricating precision.

## Core task

Try to overturn every provisional conclusion.

Specifically test whether:

- employee remittance gaps are timing artefacts;
- employer gaps come from incorrect legal rates;
- State transfers were the intended historical financing mechanism;
- the 2006 RGSS effect is smaller than claimed;
- combined deficits depend on perimeter choices;
- the 2011 bank transfer was balanced once specific State financing is included;
- the bank transfer appears adverse only under selectively chosen discount rates;
- the bank transfer remains adverse even under conservative assumptions and full legal financing.

Write `paper/falsification_report.md` before drafting the manuscript.

## Required outputs

For every substantive result produced by this task:

- preserve or register the primary source;
- write deterministic intermediate/processed data rather than leaving results only in notebook output;
- update the relevant evidence registry;
- attach units, period, accounting basis and perimeter metadata;
- record reconciliation residuals and unresolved discrepancies explicitly;
- add or update tests for deterministic transformations;
- update documentation when a definition, assumption or limitation changes.

Where the task creates a new quantitative claim, add it to `evidence/claim_registry.csv` with a falsification condition and status. A published number that has not yet been independently reconstructed must remain `to_replicate`.

## Validation requirements

At minimum, test:

- duplicate rows and double counting;
- unit and currency consistency;
- sign conventions;
- year/perimeter mismatches;
- missing values;
- source revisions;
- accounting identity residuals where applicable;
- sensitivity to reasonable alternative definitions when the result depends on a convention.

A notebook or script must fail loudly when required evidence is missing. Do not silently substitute estimates for official values.

## Completion criteria

This task is complete only when:

1. the requested evidence can be regenerated from registered sources;
2. all transformations are inspectable and typed where implemented in Python;
3. numerical outputs have deterministic tests or reconciliation checks;
4. unresolved items are listed explicitly;
5. no manuscript language overstates what the data demonstrate.
