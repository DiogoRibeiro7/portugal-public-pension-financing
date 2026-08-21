# Source Acquisition

Status: `partial_bounded_reconstruction`

Acquisition log: `evidence/source_acquisition_log.csv`

Retrieval date: 2026-08-21

## Result

This pass attempted the 16 registered official sources that did not already
have raw files. It acquired and hashed 8 usable source pages:

- Tribunal Constitucional Acórdão n.o 255/2020.
- Tribunal Constitucional Acórdão n.o 362/2016.
- CGA organic-law page.
- CGA annual-reports catalogue.
- IGFSS Social Security budget/account page.
- DGAEP SIEP page.
- DGAEP BOEP page.
- INE historical-publications catalogue.

The files are stored under `data/raw/source_catalogues/` and registered in
`evidence/source_registry.csv` with raw path, retrieval date, and SHA-256 hash.
Stored HTML captures use LF line endings so the registered hashes validate on
Windows and Linux checkouts.

## Rejected Captures

Five Diário da República detail URLs returned generic OutSystems shell HTML
rather than citable source text. Those captures are recorded in
`evidence/source_acquisition_log.csv` as `shell_html_not_evidence` and are not
marked as acquired sources in `evidence/source_registry.csv`.

## Failed Attempts

Three registered URLs were not acquired in this pass:

- DGO Conta Geral do Estado archive: SSL connection failure.
- DGO State Budget archive: SSL connection failure.
- Banco de Portugal ESA2010 statistical-series release: HTTP failure.

They remain registered source routes and need a later acquisition path. Existing
already-acquired PDFs remain unchanged.

## Gate

`validate-evidence` now checks that acquisition-log rows reference registered
sources, acquired raw files exist, hashes match the raw bytes, and successful
acquisitions match `evidence/source_registry.csv`.

This is not a complete acquisition of the 1977-2025 evidence base. It is a
bounded acquisition and hashing pass for reachable registered sources.
