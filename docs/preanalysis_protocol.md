# Freeze analysis protocol

Status: `partial_bounded_reconstruction`

The current protocol is frozen as version `0.3.0`.

The machine-readable protocol is `evidence/analysis_protocol.csv`. Its hash is recorded in
`evidence/analysis_protocol_hash.csv`.

## Scope

The protocol inventories the current confirmatory questions before final quantitative work:

- employee remittance gaps;
- employer legal contribution gaps;
- CGA closed-scheme balance mechanics;
- post-2006 public-worker RGSS contribution reallocation;
- combined CGA-RGSS balance definitions;
- counterfactual financing consistency;
- bank-transfer inception balance;
- bank special-regime State financing;
- bank liability-relief net positions;
- ESA-95 and ESA-2010 accounting treatment;
- release reproducibility gates;
- manuscript neutrality gates.

## Decision Rules

Each estimand defines numerator, denominator, population, period, unit, accounting basis,
institutional perimeter, source class, tolerance rule, materiality rule, falsification rule,
counterfactual class, and alternative perimeter set.

The protocol is still bounded: most quantitative estimands remain `defined_requires_sources` until
the missing source classes listed in `required_source_class` are acquired and extracted.

## Freeze Rule

Confirmatory notebooks should fail or stop if their estimand is absent from
`evidence/analysis_protocol.csv`, if the required source class is missing, or if the protocol hash
has changed without an intentional version update.

## Evidence Rule

This file records the current executable state only. It must not be read as a completed
quantitative finding until the required sources, extraction records, transformations, and checks
are present.
