# Publication Figures and Tables

Publication figure inputs live under `paper/figures/data/`, with one companion CSV per required figure candidate. `paper/figures/figure_registry.csv` records each candidate's source datasets, publication status and blocker.

The current artifact layer is intentionally partial. It creates companion CSVs only from validated repository data and marks candidates as blocked where the processed input is missing or incomplete. No missing historical values are imputed for plotting.

Publication table companions live under `paper/tables/` and are listed in `paper/tables/table_registry.csv`.

Run `python -m portugal_pensions.cli validate-evidence` to check figure coverage, companion CSV existence and source-dataset constraints.
