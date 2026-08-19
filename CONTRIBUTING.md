# Contributing

This repository is a reproducible research package. Contributions should improve the audit trail, source coverage, code reliability, or clarity of the manuscript without weakening the distinction between legal obligations, cash flows, actuarial liabilities, and statistical-accounting treatment.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Quality Checks

Run the complete local gate before opening a pull request:

```bash
make quality
```

The gate runs formatting checks, linting, strict type checking, unit tests, evidence-registry validation, and manifest validation.

## Research Standards

- Preserve raw sources exactly as acquired.
- Record each source in `evidence/source_registry.csv`.
- Keep employee contributions, employer contributions, State Budget transfers, asset transfers, and liabilities in separate variables.
- Map material manuscript claims to source-backed evidence records.
- Do not fill historical gaps silently; document the gap and its effect on inference.
- When adding a derived dataset, include the deterministic transformation that produced it.

## Pull Requests

Pull requests should include:

- the research or engineering purpose of the change;
- affected source, evidence, notebook, or manuscript files;
- validation commands run locally;
- any remaining uncertainty, source gap, or interpretation risk.
