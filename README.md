# Who Funded the Public Pension Promise?

## Historical financing of Portugal's CGA, Social Security, and transferred banking-sector pension liabilities

[![CI](https://github.com/DiogoRibeiro7/portugal-public-pension-financing/actions/workflows/ci.yml/badge.svg)](https://github.com/DiogoRibeiro7/portugal-public-pension-financing/actions/workflows/ci.yml)

This repository is a reproducible empirical research project on the long-run financing of Portuguese public pensions.

The project is deliberately **not** organised around a predetermined political conclusion. It distinguishes legal obligations, cash accounting, consolidated public-finance flows, actuarial liabilities, and counterfactual financing regimes before interpreting any balance as a deficit, surplus, subsidy, underfunding, or transfer.

### Main research question

> How was the pension promise made to Portuguese public-sector workers actually financed over time, and how does that financing history affect contemporary assessments of the CGA and Social Security systems?

### Additional institutional question: banking-sector pensions

The repository treats the 2009-2012 integration of banking-sector workers and pension liabilities as a separate research module.

The key legal sequence includes:

- Decree-Law 54/2009: new banking-sector workers enter the general Social Security regime.
- Decree-Law 1-A/2011: active banking-sector workers covered by CAFEB are integrated into the general regime for specified contingencies and CAFEB is extinguished.
- Decree-Law 127/2011: Social Security assumes specified pensions already in payment on 31 December 2011; assets of the relevant private pension funds are transferred to the State; the State is made responsible for financing those pensions through a specific transfer to Social Security; and the corresponding bank responsibilities become definitively and irreversibly extinguished once the transfer is made.
- Decree-Law 88/2012: special treatment for the BPN group transfers specified liabilities to CGA with corresponding financing.

The project therefore does **not** encode the proposition that the 2011 agreement was harmful to Social Security as a fact. It tests whether the transaction was ex ante actuarially balanced, whether the State subsequently financed the transferred obligations as required, whether Social Security incurred an uncompensated net burden, and how the operation affected headline public accounts.

An important published benchmark to replicate is the European Commission's later assessment that the 2011 bank-pension-fund transfer improved the ESA-95 headline deficit by about 3.5% of GDP, while under ESA-2010 the operation is treated as a financial transaction with no deficit impact. The same assessment reports roughly EUR 0.5 billion of additional pension expenditure in 2012 associated with the transferred bank pensions.

## Core distinctions

The analysis keeps the following objects separate:

1. employee contributions legally due;
2. employee deductions actually withheld;
3. employee contributions recorded as received;
4. employer contributions legally due;
5. employer contributions actually received;
6. State Budget transfers;
7. transfers of pension assets and liabilities;
8. economic counterfactual contributions;
9. actuarial liabilities;
10. institutional cash balances;
11. consolidated general-government balances;
12. statistical-accounting treatment under ESA-95 and ESA-2010.

## Target period

The preferred quantitative horizon is **1977-2025**, with documentary reconstruction before the first consistently machine-readable years. Where data quality does not support a continuous historical series, the repository must preserve the gap instead of interpolating it silently.

## Research pipeline

```text
primary sources
    -> immutable raw files
    -> source registry
    -> legal and accounting normalisation
    -> reconciliation ledgers
    -> hypothesis-specific analyses
    -> robustness/falsification
    -> article evidence package
    -> manuscript
```

## Repository layout

```text
.github/                CI, issue templates, pull request template, code ownership
config/                 analysis and source configuration
data/raw/                immutable downloaded sources
data/interim/            extracted/normalised intermediate data
data/processed/          validated analytical datasets
evidence/                source, claim, legal and reconciliation registries
notebooks/               sequential research notebooks
paper/                   manuscript scaffold and hypothesis registry
prompts/                 reproducible research prompts and audit instructions
src/portugal_pensions/   reusable research code
tests/                   deterministic unit tests
```

## Reproducibility rules

- Never overwrite a raw source.
- Never merge employee and employer contributions into one variable.
- Never call an economic counterfactual a legal debt.
- Never infer diversion or misuse of funds from a reconciliation residual alone.
- Never treat the full RGSS employer rate as a pension-only benchmark without risk adjustment.
- Never assume that a transfer of pension assets creates a free fiscal gain: transferred liabilities must remain in the same ledger.
- Never classify the 2011 banking operation from a single accounting standard; reproduce both ESA-95 and ESA-2010 treatments.
- Every important manuscript claim must map to a source and a deterministic transformation.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
make quality
python -m portugal_pensions.cli validate-evidence
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
python -m pytest
python -m portugal_pensions.cli validate-all
```

The notebooks are designed to be run in numerical order only after the corresponding source-acquisition prompt has been completed.

## Quality gate

The professional development gate is:

```bash
make quality
```

It runs:

- `ruff check src tests`
- `ruff format --check src tests`
- `mypy src/portugal_pensions`
- `pytest`
- `python -m portugal_pensions.cli validate-evidence`
- `python -m portugal_pensions.cli validate-manifest`

## Command-line utilities

```bash
portugal-pensions validate-evidence
portugal-pensions validate-manifest
portugal-pensions validate-all
```

## Citation

Use `CITATION.cff` for citation metadata. For reproducible snapshots, cite a tagged release and include the corresponding `MANIFEST.sha256` checksum file.

## Contributing

See `CONTRIBUTING.md` for development setup, research standards, and pull request expectations.
