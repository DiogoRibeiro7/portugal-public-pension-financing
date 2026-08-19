# Prepare the journal submission and independent replication package

## Objective
Create a submission-ready research artifact after all evidence and peer-review gates pass.

## Tasks
- Produce a clean replication release from raw-source retrieval through manuscript tables.
- Freeze package/environment versions and record platform information.
- Create a one-command or clearly staged replication workflow.
- Generate a data/code availability statement describing public, restricted and derived files.
- Create a compact reviewer appendix listing definitions, accounting perimeters, robustness variants and unresolved limitations.
- Verify that every table/figure in the manuscript is regenerated from code.
- Prepare an archive manifest suitable for an external repository/DOI service.

## Outputs
Create `docs/replication_guide.md`, `paper/data_code_availability.md`, `paper/reviewer_methods_appendix.md` and a release manifest.

## Acceptance criteria
An independent reviewer should be able to reproduce headline results without relying on hidden notebook state or manuscript-entered numbers.
