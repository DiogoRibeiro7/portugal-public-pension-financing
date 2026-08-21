# Add data licensing policy

Instruction file: `prompts/44_data_redistribution_licensing_and_archival_policy.md`
Date: 2026-08-21
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Added a source-by-source licensing and redistribution registry covering every registered source.
- Distinguished acquired public downloads, registered public URLs, and retrieval failures.
- Marked sources with unclear redistribution rights as metadata-and-hash release candidates only, with raw files excluded from any public release until terms are verified.
- Documented a clean-room acquisition path for replicators.
- Added validation coverage requiring all source registry IDs to appear in the licensing registry and requiring unclear raw sources to be excluded from public release packaging.
- Preserved existing validated outputs and did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Added an executable data licensing and archival policy. The current result is a bounded public-release gate: it identifies which source files can be handled with attribution under recorded terms and which must remain metadata-only until a rights review verifies redistribution permission.

## Current Stop Condition

Completion beyond this record requires institution-specific rights review for Portuguese legal, audit, statistical, and archive captures before publishing raw source files in a public release package. Until then, the public release path is metadata, hashes, citations, and clean-room retrieval instructions for those sources.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
