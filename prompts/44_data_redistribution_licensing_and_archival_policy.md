# Audit data redistribution, licensing and archival policy

## Objective
Ensure the public repository can be released without improperly redistributing restricted documents or breaking reproducibility.

## Tasks
- For every raw source record whether redistribution is clearly permitted, unclear or restricted.
- When redistribution is unclear, store retrieval metadata, hash and downloader instructions instead of republishing the file.
- Preserve stable citations and archival identifiers when available.
- Distinguish public accessibility from permission to redistribute.
- Add a clean-room data acquisition path for replicators.

## Outputs
Create `evidence/data_license_registry.csv` and `docs/data_retrieval.md`.

## Acceptance criteria
A fresh user must be able to reconstruct all redistributable inputs and identify how to obtain non-redistributable inputs legally.
