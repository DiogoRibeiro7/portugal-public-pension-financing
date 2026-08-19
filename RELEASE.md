# Release Process

Use releases to mark reproducible research snapshots.

1. Run `make quality`.
2. Regenerate derived outputs and notebook artifacts that are part of the release.
3. Update `CHANGELOG.md` with source, evidence, code, and manuscript changes.
4. Update `CITATION.cff` and `.zenodo.json` with the release version.
5. Regenerate `MANIFEST.sha256`.
6. Create a signed tag using semantic versioning, for example `v0.2.1`.
7. Create a GitHub release from that tag so Zenodo can archive it and mint the DOI.
8. Attach any permitted archival artifacts and cite the release tag or Zenodo DOI in downstream manuscripts.

Do not include restricted raw data in release artifacts unless the source license explicitly allows redistribution.

Before the first DOI can be minted, enable this repository in Zenodo's GitHub integration. Zenodo archives GitHub releases only after the repository has been enabled there.
