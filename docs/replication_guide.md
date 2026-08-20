# Replication guide

Status: `partial_bounded_reconstruction`

This guide describes the current bounded replication workflow. It does not certify the project as a
final public report.

## Environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-release.txt
pip install -e .
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-release.txt
pip install -e .
```

## Validation

```bash
make quality
python -m portugal_pensions.cli validate-all
```

`make quality` checks linting, formatting, typing, tests, evidence registries, the archive
manifest, and Zenodo metadata.

## Notebooks

Run notebooks in numeric order only after the required raw sources and processed inputs for each
step are present. A future release should archive a clean sequential execution log before claiming
notebook-regenerated results.

## Current boundary

The reproducibility report is `docs/reproducibility_report.md`. The machine-readable release
readiness audit is `data/processed/release_reproducibility_audit.csv`.
