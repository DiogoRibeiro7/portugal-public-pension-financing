# Data Retrieval And Redistribution Policy

Status: `partial_bounded_reconstruction`

This repository distinguishes public accessibility from permission to
redistribute. A public URL or a successful download is not treated as a license
to republish the raw source file unless a source-specific or institution-level
reuse rule is recorded in `evidence/data_license_registry.csv`.

## Source Families

- European Commission material is currently marked redistributable with
  attribution when no document-specific restriction is observed, following the
  Commission reuse policy.
- Banco de Portugal material is currently marked redistributable with
  attribution when reproduced accurately and cited, subject to document-specific
  checks.
- Portuguese legal, audit, institutional, statistical, and archive pages remain
  conservative by default unless a source-specific reuse rule is captured. They
  are treated as publicly accessible but not automatically redistributable.

The Portuguese administrative-document reuse framework supports open reuse
licenses, but this repository has not completed a source-by-source rights review
for every stored PDF or HTML capture. Until that review is complete, unclear
raw files must be excluded from any public release package and replaced by
retrieval metadata, hashes, citations, and extraction instructions.

## Clean-Room Acquisition Path

1. Start from `evidence/source_registry.csv`.
2. For each `source_id`, open the `download_url` or `url`.
3. Save the file only when the source can be legally obtained by the
   replicator.
4. Compute SHA-256 on the raw file and compare it with the registry when a hash
   is present.
5. If the source is registered but not acquired, record the retrieval date,
   failure mode, and any replacement official route in
   `evidence/source_acquisition_log.csv`.
6. Do not use repository raw copies for sources whose
   `redistribution_status` is `permission_unclear_do_not_redistribute` unless a
   later rights review changes the row.
7. Cite the original institution and URL in any downstream artifact that uses
   the source.

## Public Release Packaging Rule

Rows marked `allowed_with_attribution` may remain in a public archive if the
archive preserves source citation and does not include document-specific
third-party material that is separately restricted. Rows marked
`permission_unclear_do_not_redistribute` may keep metadata, hashes, derived
extraction tables, and reproducible instructions, but raw PDFs or HTML captures
must be excluded from the public release until permission is verified. Rows
marked `not_acquired_no_redistribution` are metadata-only routes.

## Current Stop Condition

The gate is complete enough to prevent accidental raw-source redistribution in
a public package, but it is not a final legal review. Before a public report or
archive release, the project still needs institution-specific rights checks for
Diario da Republica, DGO, Tribunal de Contas, Tribunal Constitucional, CGA,
IGFSS, DGAEP, and INE source captures.
