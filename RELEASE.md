# Release Process

Use releases to mark reproducible research snapshots.

1. Run `make quality`.
2. Regenerate derived outputs and notebook artifacts that are part of the release.
3. Update `CHANGELOG.md` with source, evidence, code, and manuscript changes.
4. Regenerate `MANIFEST.sha256`.
5. Create a signed tag using semantic versioning, for example `v0.2.1`.
6. Attach any permitted archival artifacts and cite the release tag in downstream manuscripts.

Do not include restricted raw data in release artifacts unless the source license explicitly allows redistribution.
