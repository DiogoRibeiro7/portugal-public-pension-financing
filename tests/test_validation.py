from pathlib import Path

from portugal_pensions.validation import (
    validate_article_evidence,
    validate_evidence_directory,
    validate_falsification_review,
    validate_internal_replication_review,
    validate_manifest,
    validate_manuscript_draft,
    validate_publication_artifacts,
    validate_release_reproducibility_audit,
    validate_source_registry,
    validate_submission_package,
    validate_zenodo_metadata,
)


def test_repository_evidence_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_evidence_directory(root / "evidence") == []


def test_repository_zenodo_metadata_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_zenodo_metadata(root / ".zenodo.json") == []


def test_repository_falsification_review_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_falsification_review(root / "data" / "processed" / "falsification_review.csv")
        == []
    )


def test_repository_publication_artifacts_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_publication_artifacts(
            root / "paper" / "figures" / "figure_registry.csv",
            root / "paper" / "tables" / "table_registry.csv",
            root,
        )
        == []
    )


def test_repository_article_evidence_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_article_evidence(
            root / "evidence" / "article_evidence.csv",
            root / "evidence" / "claim_registry.csv",
            root / "evidence" / "figure_registry.csv",
            root / "evidence" / "table_registry.csv",
            root,
        )
        == []
    )


def test_repository_manuscript_draft_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_manuscript_draft(
            root / "paper" / "manuscript.tex",
            root / "evidence" / "article_evidence.csv",
        )
        == []
    )


def test_repository_internal_replication_review_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_internal_replication_review(
            root / "data" / "processed" / "internal_replication_review.csv",
            root / "evidence" / "article_evidence.csv",
        )
        == []
    )


def test_repository_release_reproducibility_audit_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_release_reproducibility_audit(
            root / "data" / "processed" / "release_reproducibility_audit.csv",
            root,
        )
        == []
    )


def test_repository_submission_package_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_submission_package(
            root / "data" / "processed" / "submission_package_manifest.csv",
            root,
        )
        == []
    )


def test_manuscript_draft_requires_article_evidence_references(tmp_path: Path) -> None:
    manuscript = tmp_path / "manuscript.tex"
    article = tmp_path / "article_evidence.csv"
    article.write_text(
        "evidence_id,claim_id\nAE_REQUIRED,CLAIM\n",
        encoding="utf-8",
    )
    manuscript.write_text(
        "[Legal fact]\n"
        "[Accounting fact]\n"
        "[Interpretation]\n"
        "[Unresolved evidence]\n"
        "[Counterfactual result]\n"
        "[Actuarial assumption]\n"
        "does not yet support definitive claims\n"
        "does not establish\n"
        "does not classify\n"
        "No numerical counterfactual result is reported\n",
        encoding="utf-8",
    )

    assert (
        "Manuscript does not reference article evidence row: AE_REQUIRED"
        in validate_manuscript_draft(manuscript, article)
    )


def test_internal_replication_review_requires_article_claim_coverage(tmp_path: Path) -> None:
    review = tmp_path / "internal_replication_review.csv"
    article = tmp_path / "article_evidence.csv"
    article.write_text(
        "evidence_id,claim_id\nAE_REQUIRED,CLAIM_REQUIRED\n",
        encoding="utf-8",
    )
    header = (
        "review_id,target_area,target_claim_ids,input_artifacts,source_ids,period,unit,"
        "perimeter,accounting_basis,check_type,independent_result,residual,"
        "alternative_definition_effect,decision,status,blocking_issue,notes\n"
    )
    row = (
        "REPL_ACCOUNTING_IDENTITIES,area,OTHER_CLAIM,evidence/file.csv,SRC,2011,"
        "EUR_million,perimeter,basis,check,result,0.0,alternative,"
        "replicated_bounded,partial_bounded_review,none,notes\n"
    )
    review.write_text(header + row, encoding="utf-8")

    errors = validate_internal_replication_review(review, article)
    assert "Article evidence claim missing replication review: CLAIM_REQUIRED" in errors


def test_release_reproducibility_audit_requires_pinned_requirements(tmp_path: Path) -> None:
    audit = tmp_path / "release_reproducibility_audit.csv"
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("ok\n", encoding="utf-8")
    (tmp_path / "requirements-release.txt").write_text("pandas>=2\n", encoding="utf-8")
    audit.write_text(
        "check_id,release_area,input_artifacts,command_or_gate,period,unit,perimeter,"
        "accounting_basis,result,status,blocking_issue,notes\n"
        "REL_QUALITY_GATE,quality,artifact.txt,gate,none,none,repo,basis,result,"
        "ready,none,notes\n",
        encoding="utf-8",
    )

    errors = validate_release_reproducibility_audit(audit, tmp_path)
    assert "Unpinned release requirement on line 1: pandas>=2" in errors


def test_submission_package_requires_bounded_status_blocker(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.md"
    artifact.write_text("bounded research snapshot\n", encoding="utf-8")
    manifest = tmp_path / "submission_package_manifest.csv"
    manifest.write_text(
        "item_id,artifact_path,artifact_role,required_for_submission,current_status,"
        "blocking_issue,validation_gate,notes\n"
        "SUB_REPLICATION_GUIDE,artifact.md,guide,yes,partial_bounded,none,gate,notes\n",
        encoding="utf-8",
    )

    errors = validate_submission_package(manifest, tmp_path)
    assert "Partial submission package row SUB_REPLICATION_GUIDE must name a blocker" in errors


def test_article_evidence_rejects_blocking_claim_status(tmp_path: Path) -> None:
    evidence_dir = tmp_path / "evidence"
    data_dir = tmp_path / "data" / "processed"
    figure_dir = tmp_path / "paper" / "figures" / "data"
    evidence_dir.mkdir()
    data_dir.mkdir(parents=True)
    figure_dir.mkdir(parents=True)
    dataset = data_dir / "dataset.csv"
    dataset.write_text("value\n1\n", encoding="utf-8")
    companion = figure_dir / "fig.csv"
    companion.write_text("figure_id,value,status\nFIG01,1,ready_partial\n", encoding="utf-8")
    claim_registry = evidence_dir / "claim_registry.csv"
    claim_registry.write_text(
        "claim_id,topic,claim_text,claim_type,source_id,status,"
        "falsification_condition,manuscript_section\n"
        "CLAIM,topic,text,published_quantitative_claim,SRC,to_replicate,"
        "condition,1\n",
        encoding="utf-8",
    )
    article = evidence_dir / "article_evidence.csv"
    article.write_text(
        "evidence_id,claim_id,manuscript_section,claim_status,source_ids,raw_value,"
        "transformation,processed_dataset,output_artifact,unit,provenance_status,notes\n"
        "AE,CLAIM,1,to_replicate,SRC,1,copy,data/processed/dataset.csv,"
        "paper/figures/data/fig.csv,EUR_million,ready_for_bounded_article_use,notes\n",
        encoding="utf-8",
    )
    figure_registry = evidence_dir / "figure_registry.csv"
    figure_registry.write_text(
        "figure_id,title,companion_csv,source_datasets,publication_status,"
        "primary_blocker,article_use_status,notes\n"
        "FIG01,Title,paper/figures/data/fig.csv,data/processed/dataset.csv,"
        "ready_partial,none,bounded_article_use,notes\n",
        encoding="utf-8",
    )
    table_registry = evidence_dir / "table_registry.csv"
    table_registry.write_text(
        "table_id,title,companion_csv,source_datasets,publication_status,"
        "article_use_status,notes\n",
        encoding="utf-8",
    )

    errors = validate_article_evidence(
        article,
        claim_registry,
        figure_registry,
        table_registry,
        tmp_path,
    )
    assert "Article evidence AE uses blocking claim status: to_replicate" in errors


def test_publication_artifacts_require_all_figures(tmp_path: Path) -> None:
    figure_dir = tmp_path / "paper" / "figures"
    table_dir = tmp_path / "paper" / "tables"
    figure_data = figure_dir / "data"
    figure_data.mkdir(parents=True)
    table_dir.mkdir(parents=True)
    companion = figure_data / "fig01.csv"
    companion.write_text(
        "figure_id,series,value,status\nFIG01,series,1.0,ready_partial\n",
        encoding="utf-8",
    )
    figure_registry = figure_dir / "figure_registry.csv"
    figure_registry.write_text(
        "figure_id,title,companion_csv,source_datasets,publication_status,"
        "primary_blocker,notes\n"
        "FIG01,Title,paper/figures/data/fig01.csv,data/processed/source.csv,"
        "ready_partial,none,notes\n",
        encoding="utf-8",
    )
    table_registry = table_dir / "table_registry.csv"
    table_registry.write_text(
        "table_id,title,companion_csv,source_datasets,publication_status,notes\n",
        encoding="utf-8",
    )

    errors = validate_publication_artifacts(figure_registry, table_registry, tmp_path)
    assert "Missing required publication figure: FIG02" in errors


def test_falsification_review_requires_all_challenges(tmp_path: Path) -> None:
    review = tmp_path / "falsification_review.csv"
    review.write_text(
        "test_id,challenge,target_module,adversarial_hypothesis,evidence_required,"
        "current_evidence,result_class,decision,unit,source_ids,blocking_issue,status,notes\n"
        "FALS_001,Challenge,module,hypothesis,evidence,current,not_testable_yet,"
        "unresolved_requires_sources,EUR_million,SRC,missing,blocked_missing_inputs,notes\n",
        encoding="utf-8",
    )

    assert "Missing required falsification test: FALS_002" in validate_falsification_review(review)


def test_manifest_validation_accepts_matching_hash(tmp_path: Path) -> None:
    payload = tmp_path / "payload.txt"
    payload.write_bytes(b"reproducible\n")
    manifest = tmp_path / "MANIFEST.sha256"
    manifest.write_text(
        "9eea221f83299a3ebea16d547cb0f1cbbaace6be5c925cd9f0ccfcd1b6549c67  ./payload.txt\n",
        encoding="utf-8",
    )

    assert validate_manifest(manifest, tmp_path) == []


def test_manifest_validation_normalizes_text_line_endings(tmp_path: Path) -> None:
    payload = tmp_path / "payload.csv"
    payload.write_bytes(b"column\r\nvalue\r\n")
    manifest = tmp_path / "MANIFEST.sha256"
    manifest.write_text(
        "026cca97661612db545eba77bd301821146b2029d14d4082890565d9efef91ea  ./payload.csv\n",
        encoding="utf-8",
    )

    assert validate_manifest(manifest, tmp_path) == []


def test_manifest_validation_reports_mismatch(tmp_path: Path) -> None:
    payload = tmp_path / "payload.txt"
    payload.write_bytes(b"changed\n")
    manifest = tmp_path / "MANIFEST.sha256"
    manifest.write_text(f"{'0' * 64}  ./payload.txt\n", encoding="utf-8")

    assert validate_manifest(manifest, tmp_path) == ["Checksum mismatch for ./payload.txt"]


def test_source_registry_accepts_acquired_file(tmp_path: Path) -> None:
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    source = raw_dir / "source.pdf"
    source.write_bytes(b"%PDF-1.6\n")
    registry = tmp_path / "source_registry.csv"
    registry.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,Source,Institution,primary,2026,https://example.test,"
        "https://example.test/source.pdf,2026-08-19,2026,source,"
        "data/raw/source.pdf,"
        "9082eec5c6ba6e190d38f6014d2e8cfabb0abb2943bb3af1c5437f227590a49a,"
        "acquired,Test source\n",
        encoding="utf-8",
    )

    assert validate_source_registry(registry, tmp_path) == []


def test_source_registry_reports_missing_raw_file(tmp_path: Path) -> None:
    registry = tmp_path / "source_registry.csv"
    registry.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,Source,Institution,primary,2026,https://example.test,"
        "https://example.test/source.pdf,2026-08-19,2026,source,"
        "data/raw/source.pdf,"
        "60b1c307209d5ed068dbb745b6e03e7a13bd447936c98931791a833998e8c25f,"
        "acquired,Test source\n",
        encoding="utf-8",
    )

    assert validate_source_registry(registry, tmp_path) == [
        "Source SRC raw file is missing: data/raw/source.pdf"
    ]


def test_source_registry_reports_checksum_mismatch(tmp_path: Path) -> None:
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    source = raw_dir / "source.pdf"
    source.write_bytes(b"changed\n")
    registry = tmp_path / "source_registry.csv"
    registry.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,Source,Institution,primary,2026,https://example.test,"
        "https://example.test/source.pdf,2026-08-19,2026,source,"
        f"data/raw/source.pdf,{'0' * 64},acquired,Test source\n",
        encoding="utf-8",
    )

    assert validate_source_registry(registry, tmp_path) == [
        "Source SRC checksum mismatch for data/raw/source.pdf"
    ]


def test_zenodo_metadata_requires_creator(tmp_path: Path) -> None:
    metadata = tmp_path / ".zenodo.json"
    metadata.write_text(
        '{"title": "Project", "upload_type": "software", "description": "Test", '
        '"version": "0.1.0", "license": "mit", "creators": []}',
        encoding="utf-8",
    )

    assert validate_zenodo_metadata(metadata) == ["Zenodo metadata requires at least one creator"]
