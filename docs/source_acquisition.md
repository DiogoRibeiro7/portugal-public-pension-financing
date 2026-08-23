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

A later 2026-08-23 acquisition added official CGA annual report PDFs:

- `CGA_REPORT_2024`, stored at `data/raw/cga/CGA_REPORT_2024.pdf`.
- SHA-256:
  `9c32c61e76beb3d2d165408f1fa8c3135df1dfd7a4f908c9a932424e6a67f8b6`.
- `CGA_REPORT_2023`, stored at `data/raw/cga/CGA_REPORT_2023.pdf`.
- SHA-256:
  `85fbb2cce0614a498b653c8d1b3bdf8aedb8b62f025d5f75d5016b832df6a780`.
- `CGA_REPORT_2022`, stored at `data/raw/cga/CGA_REPORT_2022.pdf`.
- SHA-256:
  `1b0534dc566554e5552ced83edd98b4667ce07f08382030e7d13ed1d35dbe21f`.
- `CGA_REPORT_2021`, stored at `data/raw/cga/CGA_REPORT_2021.pdf`.
- SHA-256:
  `2eb34ec9f3f8395b835bbab972609595973d81d7cb472d054bcd6d11a3d5adb4`.
- `CGA_REPORT_2020`, stored at `data/raw/cga/CGA_REPORT_2020.pdf`.
- SHA-256:
  `c2f38f94562b435d53445f32160eee3f8bfab8cb405c6b7e164a769ae9b588ca`.
- `CGA_REPORT_2019`, stored at `data/raw/cga/CGA_REPORT_2019.pdf`.
- SHA-256:
  `d1cddb2be48ee7b2e68d0fab5fdda4cbefaa6ffd4558124177e922b9aad4ef26`.
- `CGA_REPORT_2018`, stored at `data/raw/cga/CGA_REPORT_2018.pdf`.
- SHA-256:
  `2220e00ffa8f293295437fd63fdc6ac17fb86444f08e22ff1727904d0a97043f`.
- `CGA_REPORT_2017`, stored at `data/raw/cga/CGA_REPORT_2017.pdf`.
- SHA-256:
  `aa2faf17a9ca2f44b1c9777ddf94e2d722104ddff9174d6c14e5e6350a307567`.
- `CGA_REPORT_2016`, stored at `data/raw/cga/CGA_REPORT_2016.pdf`.
- SHA-256:
  `94d6e123a50563c28aaaec20a6044a79d2d5c6b55cd916d2f2d44b49354dfbf3`.
- `CGA_REPORT_2015`, stored at `data/raw/cga/CGA_REPORT_2015.pdf`.
- SHA-256:
  `e2e78ab9600edc5cb7c33bfcab60515f573c81dedb1f4a271547fa2453d14382`.
- `CGA_REPORT_2014`, stored at `data/raw/cga/CGA_REPORT_2014.pdf`.
- SHA-256:
  `9b900d2d4cfd0dfd474b82b3548d4d5d340de6d951f2824ad1a37dca7b2b4aef`.
- `CGA_REPORT_2013`, stored at `data/raw/cga/CGA_REPORT_2013.pdf`.
- SHA-256:
  `b5a598dfd651cd7f2e1df7beae5a924ef8c4bad71a8785960244da2c7c6751f1`.
- `CGA_REPORT_2012`, stored at `data/raw/cga/CGA_REPORT_2012.pdf`.
- SHA-256:
  `2d5128f40218888edb429a0d5245f8e54550a5d3923daa6356a1b8b4e1170306`.
- `CGA_REPORT_2011`, stored at `data/raw/cga/CGA_REPORT_2011.pdf`.
- SHA-256:
  `55539f9c57a7509a2111144dd364b926e3a2e1fbb53cac8bf90bff3a0f87550a`.
- Selected 2011-2024 financing, expenditure, and population values were extracted
  into `data/processed/cga_financing_ledger.csv` and audited in
  `evidence/extraction_audit.csv`.

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
