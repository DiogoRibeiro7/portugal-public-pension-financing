# Release Process

Use releases to mark reproducible research snapshots.

Run `data/processed/release_reproducibility_audit.csv` and
`docs/reproducibility_report.md` as the readiness gate before creating a tag. A readiness audit may
pass partially while the project remains unsuitable for a public report.

1. Run `make quality`.
2. Regenerate derived outputs and notebook artifacts that are part of the release and archive a
   clean sequential notebook execution log.
3. Update `CHANGELOG.md` with source, evidence, code, and manuscript changes.
4. Update `CITATION.cff` and `.zenodo.json` with the release version.
5. Regenerate `MANIFEST.sha256`.
   The manifest deliberately excludes dependency-pin files (`pyproject.toml`,
   `requirements-release.txt`), workflow action pins (`.github/workflows/ci.yml`) and the
   built `paper/manuscript.pdf`. Automated dependency updates rewrite the first three but
   cannot regenerate the manifest, and the PDF embeds a fresh timestamp on every build, so
   covering them would fail the integrity gate on files whose integrity git already carries.
   The exclusion list is enforced in both directions by `MANIFEST_EXCLUDED_PATHS`.
6. Create a signed tag using semantic versioning, for example `v0.2.1`.
7. Create a GitHub release from that tag so Zenodo can archive it and mint the DOI.
8. Attach any permitted archival artifacts and cite the release tag or Zenodo DOI in downstream manuscripts.

Do not include restricted raw data in release artifacts unless the source license explicitly allows redistribution.
Raw files marked `permission_unclear_do_not_redistribute` remain local-only; release archives keep
their source URLs and SHA-256 hashes in the evidence registries plus any tracked derived extracts.

Before the first DOI can be minted, enable this repository in Zenodo's GitHub integration. Zenodo archives GitHub releases only after the repository has been enabled there.
