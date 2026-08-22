from pathlib import Path

from portugal_pensions.validation import (
    validate_analysis_protocol,
    validate_article_evidence,
    validate_article_evidence_claim_boundaries,
    validate_claim_language_audit,
    validate_combined_balance_replication,
    validate_concept_registry,
    validate_conflict_and_uncertainty_registries,
    validate_data_license_registry,
    validate_evidence_directory,
    validate_extraction_audit,
    validate_falsification_decision_requirements,
    validate_falsification_review,
    validate_internal_replication_review,
    validate_joint_balance_definitions,
    validate_literature_map,
    validate_manifest,
    validate_manuscript_draft,
    validate_manuscript_section_boundaries,
    validate_public_claim_registry,
    validate_publication_artifact_readiness,
    validate_publication_artifacts,
    validate_release_reproducibility_audit,
    validate_source_acquisition_log,
    validate_source_coverage_matrix,
    validate_source_registry,
    validate_submission_package,
    validate_unit_registry,
    validate_zenodo_metadata,
)


def test_repository_evidence_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_evidence_directory(root / "evidence") == []


def test_repository_zenodo_metadata_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_zenodo_metadata(root / ".zenodo.json") == []


def test_repository_analysis_protocol_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_analysis_protocol(
            root / "evidence" / "analysis_protocol.csv",
            root / "evidence" / "analysis_protocol_hash.csv",
        )
        == []
    )


def test_repository_concept_registry_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_concept_registry(root / "evidence" / "concept_registry.csv", root) == []


def test_repository_literature_map_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_literature_map(
            root / "evidence" / "literature_map.csv",
            root / "docs" / "literature_search_protocol.md",
            root / "docs" / "related_work_synthesis.md",
        )
        == []
    )


def test_repository_source_coverage_matrix_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_source_coverage_matrix(
            root / "evidence" / "source_coverage_matrix.csv",
            root / "evidence" / "source_registry.csv",
            root / "docs" / "historical_data_gap_map.md",
        )
        == []
    )


def test_repository_source_acquisition_log_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_source_acquisition_log(
            root / "evidence" / "source_acquisition_log.csv",
            root / "evidence" / "source_registry.csv",
            root,
        )
        == []
    )


def test_repository_data_license_registry_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_data_license_registry(
            root / "evidence" / "data_license_registry.csv",
            root / "evidence" / "source_registry.csv",
        )
        == []
    )


def test_repository_extraction_audit_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_extraction_audit(
            root / "evidence" / "extraction_audit.csv",
            root / "evidence" / "source_registry.csv",
        )
        == []
    )


def test_repository_unit_registry_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert validate_unit_registry(root / "evidence" / "unit_registry.csv", root) == []


def test_repository_conflict_and_uncertainty_registries_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_conflict_and_uncertainty_registries(
            root / "evidence" / "source_conflict_registry.csv",
            root / "evidence" / "uncertainty_registry.csv",
            root / "evidence" / "source_registry.csv",
            root / "evidence" / "concept_registry.csv",
            root / "evidence" / "unit_registry.csv",
        )
        == []
    )


def test_repository_falsification_review_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_falsification_review(root / "data" / "processed" / "falsification_review.csv")
        == []
    )


def test_repository_falsification_decision_requirements_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_falsification_decision_requirements(
            root / "evidence" / "falsification_decision_requirements.csv"
        )
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


def test_repository_publication_artifact_readiness_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_publication_artifact_readiness(
            root / "evidence" / "publication_artifact_readiness_requirements.csv",
            root,
        )
        == []
    )


def test_repository_public_claim_registry_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_public_claim_registry(
            root / "evidence" / "public_claim_registry.csv",
            root / "data" / "processed" / "working_group_2026_replication.csv",
        )
        == []
    )


def test_repository_combined_balance_replication_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_combined_balance_replication(
            root / "data" / "processed" / "combined_balance_replication_2026.csv",
            root / "data" / "processed" / "combined_balance_component_bridge_2026.csv",
        )
        == []
    )


def test_repository_joint_balance_definitions_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_joint_balance_definitions(
            root / "data" / "processed" / "joint_balance_definitions.csv",
            root / "data" / "processed" / "joint_balance_definition_rules.csv",
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


def test_repository_article_evidence_claim_boundaries_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_article_evidence_claim_boundaries(
            root / "evidence" / "article_evidence_claim_boundaries.csv",
            root / "evidence" / "article_evidence.csv",
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


def test_repository_manuscript_section_boundaries_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_manuscript_section_boundaries(
            root / "paper" / "manuscript.tex",
            root / "evidence" / "manuscript_section_boundaries.csv",
            root / "evidence" / "article_evidence_claim_boundaries.csv",
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


def test_repository_claim_language_audit_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (
        validate_claim_language_audit(
            root / "data" / "processed" / "manuscript_claim_language_audit.csv",
            root / "paper" / "manuscript.tex",
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


def test_manuscript_section_boundaries_reject_overclaims(tmp_path: Path) -> None:
    manuscript = tmp_path / "manuscript.tex"
    manuscript.write_text(
        "\\section{Introduction}\n"
        "\\paragraph{[Interpretation]}\n"
        "% AE_KNOWN\n"
        "This is a definitive remittance loss.\n",
        encoding="utf-8",
    )
    boundaries = tmp_path / "manuscript_section_boundaries.csv"
    boundaries.write_text(
        "section_id,section_title,required_labels,required_evidence_ids,"
        "permitted_claim_class,blocked_claim_class,dependency_gate,status,notes\n"
        "MS_INTRO,Introduction,[Interpretation],AE_MISSING,claim,weak wording,"
        "not_applicable,complete,notes\n",
        encoding="utf-8",
    )
    article_boundaries = tmp_path / "article_evidence_claim_boundaries.csv"
    article_boundaries.write_text(
        "evidence_id,claim_id,output_artifact,required_source_transform,"
        "permitted_article_use,blocked_inference,boundary_status,dependency_gate,notes\n"
        "AE_KNOWN,CLAIM,artifact,transform,bounded_article_use,complete claim,"
        "ready_for_bounded_article_use,gate,notes\n",
        encoding="utf-8",
    )

    errors = validate_manuscript_section_boundaries(
        manuscript,
        boundaries,
        article_boundaries,
    )
    assert "Missing manuscript section boundary: MS_ACCOUNTING" in errors
    assert "Unexpected manuscript section status on row 2" in errors
    assert "Manuscript section MS_INTRO uses unknown evidence boundary AE_MISSING" in errors
    assert "Manuscript section MS_INTRO does not reference AE_MISSING" in errors
    assert "Manuscript section MS_INTRO must block overclaim language" in errors
    assert "Manuscript section MS_INTRO must name dependency gate" in errors
    assert (
        "Manuscript contains blocked section-boundary phrase: definitive remittance loss" in errors
    )


def test_analysis_protocol_rejects_hash_mismatch(tmp_path: Path) -> None:
    protocol = tmp_path / "analysis_protocol.csv"
    hash_file = tmp_path / "analysis_protocol_hash.csv"
    protocol.write_text(
        "hypothesis_id,estimand_id,formula,numerator,denominator,population,period,unit,"
        "accounting_basis,perimeter,primary_sources,tolerance_rule,materiality_rule,"
        "falsification_rule,exploratory_or_confirmatory,counterfactual_class,"
        "alternative_perimeter_set,required_source_class,protocol_version,status\n"
        "H1,E,formula,num,den,pop,period,unit,basis,perimeter,sources,tolerance,"
        "material if threshold exceeded,falsification,confirmatory,not_applicable,"
        "not_applicable,sources,0.3.0,defined_requires_sources\n",
        encoding="utf-8",
    )
    hash_file.write_text(
        "protocol_version,artifact_path,sha256,status,notes\n"
        f"0.3.0,evidence/analysis_protocol.csv,{'0' * 64},protocol_frozen,notes\n",
        encoding="utf-8",
    )

    assert (
        "Analysis protocol hash does not match analysis_protocol.csv"
        in validate_analysis_protocol(protocol, hash_file)
    )


def test_concept_registry_requires_material_column_mapping(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    processed = tmp_path / "data" / "processed"
    evidence.mkdir()
    processed.mkdir(parents=True)
    (processed / "cga_financing_ledger.csv").write_text(
        "state_budget_transfers\n1\n",
        encoding="utf-8",
    )
    registry = evidence / "concept_registry.csv"
    registry.write_text(
        "concept_id,source_label,canonical_name,concept_class,definition,valid_from,valid_to,"
        "institutional_perimeter,accounting_basis,source_id,source_definition_status,"
        "sign_convention,internal_variable_names,material_flow_columns,ambiguous_label_guard,"
        "notes\n"
        "STATE_TRANSFER,transfer,state_budget_transfer,flow,definition,1977,,perimeter,basis,,"
        "working_definition_requires_source,positive_inflow_to_recipient,state_budget_transfers,"
        "none,guard,notes\n",
        encoding="utf-8",
    )

    errors = validate_concept_registry(registry, tmp_path)
    assert (
        "Missing concept mapping for material column: "
        "data/processed/cga_financing_ledger.csv:state_budget_transfers"
    ) in errors


def test_literature_map_rejects_unsupported_novelty_language(tmp_path: Path) -> None:
    literature = tmp_path / "literature_map.csv"
    protocol = tmp_path / "literature_search_protocol.md"
    synthesis = tmp_path / "related_work_synthesis.md"
    protocol.write_text(
        "evidence of absence is not proof of novelty\n",
        encoding="utf-8",
    )
    synthesis.write_text(
        "evidence of absence is not proof of novelty\n",
        encoding="utf-8",
    )
    literature.write_text(
        "reference_id,title,year,authors,venue,source_category,topic,research_question,"
        "method,data_period,data_source,main_finding,relation_to_paper,novelty_role,"
        "inclusion_decision,search_database,search_query,search_date,source_url,notes\n"
        "LIT_TEST,Title,2020,Authors,Venue,academic_literature,topic,question,method,"
        "period,data,finding,no paper has been seen doing this,nearest_neighbor,"
        "included_nearest_neighbor,web,query,2026-08-21,https://example.test,notes\n",
        encoding="utf-8",
    )

    errors = validate_literature_map(literature, protocol, synthesis)
    assert "Literature row LIT_TEST uses unsupported novelty language" in errors


def test_source_coverage_matrix_requires_complete_horizon(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    docs = tmp_path / "docs"
    evidence.mkdir()
    docs.mkdir()
    source_registry = evidence / "source_registry.csv"
    source_registry.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,Source,Institution,official,2026,https://example.test,https://example.test,"
        "2026-08-21,1977-2025,basis,,,registered,notes\n",
        encoding="utf-8",
    )
    gap_map = docs / "historical_data_gap_map.md"
    gap_map.write_text(
        "Secondary estimates\n"
        "bank_asset_liability_transfer_schedules bank_pension_transfer_legal "
        "cga_employee_employer_revenue_split cga_reports_accounts "
        "cga_subscriber_pensioner_counts cge_public_accounts "
        "esa_pension_transfer_treatment legal_contribution_rules "
        "public_employment_counts public_worker_cohort_inputs social_security_accounts "
        "state_budget_documents\n",
        encoding="utf-8",
    )
    matrix = evidence / "source_coverage_matrix.csv"
    matrix.write_text(
        "variable_id,year,source_id,coverage_status,format,granularity,definition_break,"
        "revision_status,notes\n"
        "cge_public_accounts,1977,SRC,observed,pdf,annual,none,none,notes\n",
        encoding="utf-8",
    )

    errors = validate_source_coverage_matrix(matrix, source_registry, gap_map)
    assert "Missing source coverage row: cge_public_accounts 1978" in errors


def test_source_acquisition_log_rejects_hash_mismatch(tmp_path: Path) -> None:
    raw_dir = tmp_path / "data" / "raw" / "source_catalogues"
    evidence_dir = tmp_path / "evidence"
    raw_dir.mkdir(parents=True)
    evidence_dir.mkdir()
    raw_file = raw_dir / "SRC.html"
    raw_file.write_text("changed\n", encoding="utf-8")
    registry = evidence_dir / "source_registry.csv"
    registry.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,Source,Institution,official,2026,https://example.test,https://example.test,"
        "2026-08-21,2026,basis,data/raw/source_catalogues/SRC.html,"
        f"{'0' * 64},acquired,notes\n",
        encoding="utf-8",
    )
    log = evidence_dir / "source_acquisition_log.csv"
    log.write_text(
        "source_id,attempted_url,retrieval_date,raw_path,sha256,status,notes\n"
        "SRC,https://example.test,2026-08-21,data/raw/source_catalogues/SRC.html,"
        f"{'0' * 64},acquired,notes\n",
        encoding="utf-8",
    )

    errors = validate_source_acquisition_log(log, registry, tmp_path)
    assert "Source acquisition hash mismatch: SRC" in errors


def test_data_license_registry_requires_public_release_exclusion_for_unclear_raw(
    tmp_path: Path,
) -> None:
    source_registry = tmp_path / "source_registry.csv"
    source_registry.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,Source,Institution,official,2026,https://example.test,"
        "https://example.test/source.pdf,2026-08-21,2026,basis,data/raw/source.pdf,"
        f"{'0' * 64},acquired,notes\n",
        encoding="utf-8",
    )
    license_registry = tmp_path / "data_license_registry.csv"
    license_registry.write_text(
        "source_id,access_status,redistribution_status,license_or_terms,retrieval_method,"
        "archival_reference,clean_room_instruction,repository_action,notes\n"
        "SRC,acquired_public_download,permission_unclear_do_not_redistribute,"
        "terms not captured,download registered URL,sha256 recorded in source registry,"
        "follow source_registry download_url,retain_raw_in_public_release,notes\n",
        encoding="utf-8",
    )

    errors = validate_data_license_registry(license_registry, source_registry)
    assert "Unclear redistribution source SRC must exclude raw file from public release" in errors


def test_unit_registry_rejects_unregistered_observed_unit(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    processed = tmp_path / "data" / "processed"
    evidence.mkdir()
    processed.mkdir(parents=True)
    registry = evidence / "unit_registry.csv"
    registry.write_text(
        "unit_id,currency,scale,price_basis,base_year,flow_or_stock,accounting_basis,"
        "conversion_rule,valid_from,valid_to,canonical_unit,join_family,notes\n"
        "EUR_million,EUR,million,current_prices,,flow,any_registered_basis,none,1999,,"
        "EUR_million,nominal_money,notes\n",
        encoding="utf-8",
    )
    (processed / "dataset.csv").write_text("unit\nmystery_unit\n", encoding="utf-8")

    errors = validate_unit_registry(registry, tmp_path)
    assert "Observed CSV unit is missing from unit registry: mystery_unit" in errors


def test_conflict_uncertainty_registry_requires_unresolved_range_without_central(
    tmp_path: Path,
) -> None:
    source_registry = tmp_path / "source_registry.csv"
    source_registry.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC_A,Source A,Institution,official,2026,https://example.test/a,"
        "https://example.test/a,2026-08-21,2026,basis,,,registered,notes\n"
        "SRC_B,Source B,Institution,official,2026,https://example.test/b,"
        "https://example.test/b,2026-08-21,2026,basis,,,registered,notes\n",
        encoding="utf-8",
    )
    concept_registry = tmp_path / "concept_registry.csv"
    concept_registry.write_text(
        "concept_id,source_label,canonical_name,concept_class,definition,valid_from,valid_to,"
        "institutional_perimeter,accounting_basis,source_id,source_definition_status,"
        "sign_convention,internal_variable_names,material_flow_columns,ambiguous_label_guard,"
        "notes\n"
        "PENSION_EXPENDITURE,label,pension_expenditure,flow,definition,1977,,perimeter,"
        "basis,SRC_A,source_defined,positive_outflow,,none,guard,notes\n",
        encoding="utf-8",
    )
    unit_registry = tmp_path / "unit_registry.csv"
    unit_registry.write_text(
        "unit_id,currency,scale,price_basis,base_year,flow_or_stock,accounting_basis,"
        "conversion_rule,valid_from,valid_to,canonical_unit,join_family,notes\n"
        "EUR_million,EUR,million,current_prices,,flow,any_registered_basis,none,1999,,"
        "EUR_million,nominal_money,notes\n",
        encoding="utf-8",
    )
    conflict_registry = tmp_path / "source_conflict_registry.csv"
    conflict_registry.write_text(
        "conflict_id,concept_id,period,source_id_a,value_a,source_id_b,value_b,unit,"
        "difference_type,tolerance_rule,materiality_rule,resolution,status,uncertainty_id,"
        "notes\n"
        "CONF,PENSION_EXPENDITURE,2026,SRC_A,1,SRC_B,3,EUR_million,unresolved,"
        "no tolerance,material if unresolved,propagate range,unresolved_range,UNC,notes\n",
        encoding="utf-8",
    )
    uncertainty_registry = tmp_path / "uncertainty_registry.csv"
    uncertainty_registry.write_text(
        "estimate_id,source_or_model,lower,central,upper,unit,uncertainty_reason,method,"
        "status\n"
        "UNC,SRC_A;SRC_B,1,2,3,EUR_million,unresolved difference,propagate range,"
        "unresolved_range\n",
        encoding="utf-8",
    )

    errors = validate_conflict_and_uncertainty_registries(
        conflict_registry,
        uncertainty_registry,
        source_registry,
        concept_registry,
        unit_registry,
    )
    assert "Unresolved uncertainty row UNC must leave central empty" in errors


def test_extraction_audit_requires_high_impact_secondary_check(tmp_path: Path) -> None:
    registry = tmp_path / "source_registry.csv"
    registry.write_text(
        "source_id,title,institution,source_type,year,url,download_url,retrieval_date,"
        "reporting_period,accounting_basis,raw_path,sha256,status,notes\n"
        "SRC,Source,Institution,official,2026,https://example.test,https://example.test,"
        "2026-08-21,2026,basis,,,registered,notes\n",
        encoding="utf-8",
    )
    audit = tmp_path / "extraction_audit.csv"
    audit.write_text(
        "source_id,page,table_title,row_label,column_label,original_text,parsed_value,unit,"
        "extraction_method,validation_method,qa_tier,secondary_check,parsing_warning,"
        "status,notes\n"
        "SRC,1,Table,Row,Column,value 10,10,EUR_million,pdftotext,"
        "checked against total,high_impact,not_required,none,extracted,notes\n",
        encoding="utf-8",
    )

    errors = validate_extraction_audit(audit, registry)
    assert "High-impact extraction row lacks secondary check: SRC page 1 Row Column" in errors


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


def test_internal_replication_review_requires_section_language_gate(tmp_path: Path) -> None:
    review = tmp_path / "internal_replication_review.csv"
    article = tmp_path / "article_evidence.csv"
    article.write_text(
        "evidence_id,claim_id\nAE_REQUIRED,CLAIM_LANGUAGE_001\n",
        encoding="utf-8",
    )
    header = (
        "review_id,target_area,target_claim_ids,input_artifacts,source_ids,period,unit,"
        "perimeter,accounting_basis,check_type,independent_result,residual,"
        "alternative_definition_effect,decision,status,blocking_issue,notes\n"
    )
    row = (
        "REPL_SECTION_LANGUAGE_GATES,area,OTHER_CLAIM,paper/manuscript.tex,SRC,"
        "2011-2025,mixed,perimeter,basis,check,result,not_applicable,alternative,"
        "no_overstatement_detected,partial_bounded_review,none,notes\n"
    )
    review.write_text(header + row, encoding="utf-8")

    errors = validate_internal_replication_review(review, article)
    assert (
        "Section-language replication row missing input artifact: "
        "data/processed/manuscript_claim_language_audit.csv"
    ) in errors
    assert (
        "Section-language replication row missing input artifact: "
        "evidence/article_evidence_claim_boundaries.csv"
    ) in errors
    assert (
        "Section-language replication row missing input artifact: "
        "evidence/manuscript_section_boundaries.csv"
    ) in errors
    assert "Section-language replication row must cover CLAIM_LANGUAGE_001" in errors


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


def test_release_reproducibility_audit_requires_manuscript_pdf_gate(
    tmp_path: Path,
) -> None:
    audit = tmp_path / "release_reproducibility_audit.csv"
    paper_dir = tmp_path / "paper"
    paper_dir.mkdir()
    (tmp_path / "requirements-release.txt").write_text("pandas==2.3.2\n", encoding="utf-8")
    (tmp_path / "MANIFEST.sha256").write_text("hash  path\n", encoding="utf-8")
    (paper_dir / "manuscript.tex").write_text("source\n", encoding="utf-8")
    (paper_dir / "manuscript.pdf").write_bytes(b"")
    audit.write_text(
        "check_id,release_area,input_artifacts,command_or_gate,period,unit,perimeter,"
        "accounting_basis,result,status,blocking_issue,notes\n"
        "REL_MANUSCRIPT_PDF,compiled,paper/manuscript.tex,gate,none,none,repo,"
        "archive,result,ready_partial,missing_final_manuscript_inputs,notes\n",
        encoding="utf-8",
    )

    errors = validate_release_reproducibility_audit(audit, tmp_path)
    assert "Manuscript PDF release row missing input artifact: MANIFEST.sha256" in errors
    assert "Manuscript PDF release row missing input artifact: paper/manuscript.pdf" in errors
    assert "Compiled manuscript PDF artifact is empty" in errors


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


def test_claim_language_audit_rejects_count_mismatch(tmp_path: Path) -> None:
    manuscript = tmp_path / "manuscript.tex"
    audit = tmp_path / "language.csv"
    manuscript.write_text("This deficit is an accounting deficit.\n", encoding="utf-8")
    audit.write_text(
        "term,occurrence_count,concept_mapping,boundary_status,claim_ids,evidence_ids,"
        "section_boundary_ids,allowed_context,prohibited_inference,notes\n"
        "deficit,1,concept,bounded_use,CLAIM,EVIDENCE,MS_ACCOUNTING,context,inference,"
        "notes\n",
        encoding="utf-8",
    )

    errors = validate_claim_language_audit(audit, manuscript)
    assert "Claim language audit term deficit count mismatch: recorded 1, actual 2" in errors


def test_claim_language_audit_requires_section_boundaries(tmp_path: Path) -> None:
    manuscript = tmp_path / "paper" / "manuscript.tex"
    evidence_dir = tmp_path / "evidence"
    audit = tmp_path / "data" / "processed" / "language.csv"
    manuscript.parent.mkdir()
    evidence_dir.mkdir()
    audit.parent.mkdir(parents=True)
    manuscript.write_text("This deficit is bounded.\n", encoding="utf-8")
    (evidence_dir / "manuscript_section_boundaries.csv").write_text(
        "section_id,section_title,required_labels,required_evidence_ids,"
        "permitted_claim_class,blocked_claim_class,dependency_gate,status,notes\n"
        "MS_ACCOUNTING,Definitions,[Accounting fact],not_applicable,claim,"
        "definitive claim,gate,bounded_section,notes\n",
        encoding="utf-8",
    )
    audit.write_text(
        "term,occurrence_count,concept_mapping,boundary_status,claim_ids,evidence_ids,"
        "section_boundary_ids,allowed_context,prohibited_inference,notes\n"
        "deficit,1,concept,bounded_use,CLAIM,EVIDENCE,MS_UNKNOWN,context,inference,"
        "notes\n"
        "debt,1,concept,bounded_use,CLAIM,EVIDENCE,not_applicable,context,inference,"
        "notes\n",
        encoding="utf-8",
    )

    errors = validate_claim_language_audit(audit, manuscript)
    assert (
        "Claim language audit term deficit references unknown section boundary MS_UNKNOWN" in errors
    )
    assert "Claim language audit term debt count mismatch: recorded 1, actual 0" in errors
    assert "Present claim language term debt must map to a section boundary" in errors


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


def test_article_evidence_claim_boundaries_reject_overclaims(tmp_path: Path) -> None:
    article = tmp_path / "article_evidence.csv"
    article.write_text(
        "evidence_id,claim_id,manuscript_section,claim_status,source_ids,raw_value,"
        "transformation,processed_dataset,output_artifact,unit,provenance_status,notes\n"
        "AE1,CLAIM1,1,status,SRC,1,copy,data/processed/data.csv,"
        "paper/figures/data/fig.csv,EUR_million,ready_for_bounded_article_use,notes\n"
        "AE2,CLAIM2,1,status,SRC,1,copy,data/processed/data.csv,"
        "paper/figures/data/fig.csv,EUR_million,bounded_only,notes\n",
        encoding="utf-8",
    )
    boundaries = tmp_path / "article_evidence_claim_boundaries.csv"
    boundaries.write_text(
        "evidence_id,claim_id,output_artifact,required_source_transform,"
        "permitted_article_use,blocked_inference,boundary_status,dependency_gate,notes\n"
        "AE1,OTHER,paper/figures/data/other.csv,copy,free_use,minor wording,"
        "ready_for_bounded_article_use,not_applicable,notes\n"
        "AE2,CLAIM2,paper/figures/data/fig.csv,copy,bounded_article_use,"
        "complete claim,bounded_only,gate,notes\n",
        encoding="utf-8",
    )

    errors = validate_article_evidence_claim_boundaries(boundaries, article)
    assert "Article evidence boundary AE1 claim_id mismatch" in errors
    assert "Article evidence boundary AE1 output mismatch" in errors
    assert "Unexpected permitted_article_use on article evidence boundary row 2" in errors
    assert "Ready article evidence AE1 must use bounded article use" in errors
    assert "Article evidence boundary AE1 must block an overclaim class" in errors
    assert "Article evidence boundary AE1 must name dependency gate" in errors
    assert "Bounded-only article evidence AE2 must be caveated" in errors


def test_public_claim_registry_requires_all_targets(tmp_path: Path) -> None:
    claims = tmp_path / "public_claim_registry.csv"
    replication = tmp_path / "working_group_2026_replication.csv"
    claims.write_text(
        "claim_id,claim_target,claimant_or_report,report_component,claim_text,quantity,"
        "unit,period,perimeter,primary_source_ids,identification_source_ids,"
        "processed_dataset,replication_status,replicated_value,method_status,"
        "blocking_issue,notes\n"
        "WG2026_PUBLIC_WORKER_CONTRIB,post_2006_public_worker_contributions,"
        "2026_social_security_working_group,main_report,claim,,EUR_million,2006-2025,"
        "public workers,missing_primary_report,none,"
        "data/processed/working_group_2026_replication.csv,"
        "blocked_primary_source_missing,,method_not_specified,"
        "primary report missing,notes\n",
        encoding="utf-8",
    )
    replication.write_text(
        "claim_id,claim_target,input_artifacts,transformation,replication_status,"
        "replicated_value,residual,unit,blocking_issue,notes\n"
        "WG2026_PUBLIC_WORKER_CONTRIB,post_2006_public_worker_contributions,"
        "primary package,not_implemented_missing_primary_method,"
        "blocked_primary_source_missing,,,EUR_million,primary report missing,notes\n",
        encoding="utf-8",
    )

    errors = validate_public_claim_registry(claims, replication)
    assert "Missing public claim target: adjusted_2025_deficit" in errors
    assert "Missing public claim target: fefss_capitalization" in errors


def test_public_claim_registry_rejects_blocked_values(tmp_path: Path) -> None:
    claims = tmp_path / "public_claim_registry.csv"
    replication = tmp_path / "working_group_2026_replication.csv"
    claims.write_text(
        "claim_id,claim_target,claimant_or_report,report_component,claim_text,quantity,"
        "unit,period,perimeter,primary_source_ids,identification_source_ids,"
        "processed_dataset,replication_status,replicated_value,method_status,"
        "blocking_issue,notes\n"
        "WG2026_PUBLIC_WORKER_CONTRIB,post_2006_public_worker_contributions,"
        "2026_social_security_working_group,main_report,claim,10,EUR_million,2006-2025,"
        "public workers,missing_primary_report,none,"
        "data/processed/working_group_2026_replication.csv,"
        "blocked_primary_source_missing,10,method_not_specified,"
        "primary report missing,notes\n"
        "WG2026_FEFSS_CAPITALIZATION,fefss_capitalization,"
        "2026_social_security_working_group,main_report,claim,,EUR_million,2006-2025,"
        "reserve,missing_primary_report,none,"
        "data/processed/working_group_2026_replication.csv,"
        "blocked_primary_source_missing,,method_not_specified,"
        "primary report missing,notes\n"
        "WG2026_SHARE_OF_FEFSS,share_of_fefss,"
        "2026_social_security_working_group,main_report,claim,,percent,2006-2025,"
        "share,missing_primary_report,none,"
        "data/processed/working_group_2026_replication.csv,"
        "blocked_primary_source_missing,,method_not_specified,"
        "primary report missing,notes\n"
        "WG2026_COMBINED_BALANCE,combined_cga_previdential_balance,"
        "2026_social_security_working_group,main_report,claim,,EUR_million,2006-2025,"
        "combined balance,missing_primary_report,none,"
        "data/processed/working_group_2026_replication.csv,"
        "blocked_primary_source_missing,,method_not_specified,"
        "primary report missing,notes\n"
        "WG2026_ADJUSTED_2025_DEFICIT,adjusted_2025_deficit,"
        "2026_social_security_working_group,main_report,claim,,EUR_million,2025,"
        "adjusted balance,missing_primary_report,none,"
        "data/processed/working_group_2026_replication.csv,"
        "blocked_primary_source_missing,,method_not_specified,"
        "primary report missing,notes\n",
        encoding="utf-8",
    )
    replication.write_text(
        "claim_id,claim_target,input_artifacts,transformation,replication_status,"
        "replicated_value,residual,unit,blocking_issue,notes\n"
        "WG2026_PUBLIC_WORKER_CONTRIB,post_2006_public_worker_contributions,"
        "primary package,not_implemented_missing_primary_method,"
        "blocked_primary_source_missing,10,0,EUR_million,primary report missing,notes\n"
        "WG2026_FEFSS_CAPITALIZATION,fefss_capitalization,"
        "primary package,not_implemented_missing_primary_method,"
        "blocked_primary_source_missing,,,EUR_million,primary report missing,notes\n"
        "WG2026_SHARE_OF_FEFSS,share_of_fefss,"
        "primary package,not_implemented_missing_primary_method,"
        "blocked_primary_source_missing,,,percent,primary report missing,notes\n"
        "WG2026_COMBINED_BALANCE,combined_cga_previdential_balance,"
        "primary package,not_implemented_missing_primary_method,"
        "blocked_primary_source_missing,,,EUR_million,primary report missing,notes\n"
        "WG2026_ADJUSTED_2025_DEFICIT,adjusted_2025_deficit,"
        "primary package,not_implemented_missing_primary_method,"
        "blocked_primary_source_missing,,,EUR_million,primary report missing,notes\n",
        encoding="utf-8",
    )

    errors = validate_public_claim_registry(claims, replication)
    assert (
        "Blocked public claim rows must not contain copied or replicated values on row 2" in errors
    )
    assert "Blocked working group replication rows must not contain values on row 2" in errors


def test_combined_balance_replication_requires_annual_series(tmp_path: Path) -> None:
    replication = tmp_path / "combined_balance_replication_2026.csv"
    bridge = tmp_path / "combined_balance_component_bridge_2026.csv"
    replication.write_text(
        "series_id,year,definition_id,definition_role,component,value,unit,source_ids,"
        "component_bridge_ids,sign_effect_class,replication_status,blocking_issue,notes\n"
        "WG2026_REPORTED_SERIES,2025,published_working_group_definition,"
        "published_definition,reported_combined_total,,EUR_million,missing_primary_report,"
        "BR_CGA_BALANCE,sign_relevant,blocked_primary_source_missing,"
        "primary annual series missing,notes\n",
        encoding="utf-8",
    )
    bridge.write_text(
        "bridge_id,definition_id,component,component_role,operation,source_requirement,"
        "sign_effect_class,bank_special_regime_visibility,replication_status,"
        "blocking_issue,notes\n"
        "BR_CGA_BALANCE,published_working_group_definition,cga_balance,base_component,"
        "add,source,sign_relevant,not_applicable,blocked_primary_source_missing,"
        "primary source missing,notes\n",
        encoding="utf-8",
    )

    errors = validate_combined_balance_replication(replication, bridge)
    assert "Missing combined-balance definition: alternative_cga_only" in errors
    assert "Missing published combined-balance annual row: 2006" in errors
    assert "Missing combined-balance component bridge row: BR_PREVIDENTIAL_BALANCE" in errors


def test_combined_balance_replication_rejects_blocked_values(tmp_path: Path) -> None:
    replication = tmp_path / "combined_balance_replication_2026.csv"
    bridge = tmp_path / "combined_balance_component_bridge_2026.csv"
    rows = [
        (
            "WG2026_REPORTED_SERIES",
            str(year),
            "published_working_group_definition",
            "published_definition",
            "reported_combined_total",
            "10" if year == 2006 else "",
            "EUR_million",
            "missing_primary_report",
            "BR_CGA_BALANCE;BR_PREVIDENTIAL_BALANCE",
            "sign_relevant",
            "blocked_primary_source_missing",
            "primary annual series missing",
            "notes",
        )
        for year in range(2006, 2026)
    ]
    rows.extend(
        [
            (
                "WG2026_2025_ADJUSTED_DEFICIT",
                "2025",
                "published_working_group_adjusted_2025",
                "published_definition",
                "adjusted_current_balance_deficit",
                "",
                "EUR_million",
                "missing_primary_report",
                "BR_EARLY_RETIREMENT_ADJUSTMENT",
                "sign_relevant",
                "blocked_primary_source_missing",
                "primary adjustment bridge missing",
                "notes",
            ),
            (
                "ALT_CGA_ONLY_2025",
                "2025",
                "alternative_cga_only",
                "alternative_perimeter",
                "total_balance",
                "",
                "EUR_million",
                "missing_primary_report",
                "BR_CGA_BALANCE",
                "sign_relevant",
                "blocked_primary_source_missing",
                "primary balance source missing",
                "notes",
            ),
            (
                "ALT_CGA_PREVIDENTIAL_UNADJUSTED_2025",
                "2025",
                "alternative_cga_plus_previdential_unadjusted",
                "alternative_perimeter",
                "total_balance",
                "",
                "EUR_million",
                "missing_primary_report",
                "BR_CGA_BALANCE;BR_PREVIDENTIAL_BALANCE",
                "sign_relevant",
                "blocked_primary_source_missing",
                "primary balance source missing",
                "notes",
            ),
            (
                "ALT_CGA_PREVIDENTIAL_FEFSS_2025",
                "2025",
                "alternative_cga_plus_previdential_plus_fefss",
                "alternative_perimeter",
                "total_balance",
                "",
                "EUR_million",
                "missing_primary_report",
                "BR_FEFSS_FLOW_ALTERNATIVE",
                "sign_relevant",
                "blocked_primary_source_missing",
                "primary FEFSS source missing",
                "notes",
            ),
            (
                "ALT_BANK_SPECIAL_SENSITIVITY_2025",
                "2025",
                "bank_special_regime_sensitivity",
                "sensitivity",
                "total_balance_including_visible_bank_obligations",
                "",
                "EUR_million",
                "missing_primary_report",
                "BR_BANK_SPECIAL_SENSITIVITY",
                "sensitivity_only",
                "blocked_primary_source_missing",
                "primary bank source missing",
                "notes",
            ),
        ]
    )
    replication.write_text(
        "series_id,year,definition_id,definition_role,component,value,unit,source_ids,"
        "component_bridge_ids,sign_effect_class,replication_status,blocking_issue,notes\n"
        + "\n".join(",".join(row) for row in rows)
        + "\n",
        encoding="utf-8",
    )
    bridge.write_text(
        "bridge_id,definition_id,component,component_role,operation,source_requirement,"
        "sign_effect_class,bank_special_regime_visibility,replication_status,"
        "blocking_issue,notes\n"
        "BR_CGA_BALANCE,published_working_group_definition,cga_balance,base_component,"
        "add,source,sign_relevant,not_applicable,blocked_primary_source_missing,"
        "primary source missing,notes\n"
        "BR_PREVIDENTIAL_BALANCE,published_working_group_definition,previdential_balance,"
        "base_component,add,source,sign_relevant,not_applicable,"
        "blocked_primary_source_missing,primary source missing,notes\n"
        "BR_EARLY_RETIREMENT_ADJUSTMENT,published_working_group_adjusted_2025,"
        "early_retirement_adjustment,adjustment,adjust,source,sign_relevant,"
        "not_applicable,blocked_primary_source_missing,primary source missing,notes\n"
        "BR_OTHER_RECLASSIFICATIONS,published_working_group_definition,"
        "other_reclassifications,reclassification,reclassify,source,sign_relevant,"
        "not_applicable,blocked_primary_source_missing,primary source missing,notes\n"
        "BR_FEFSS_FLOW_ALTERNATIVE,alternative_cga_plus_previdential_plus_fefss,"
        "fefss_annual_flow,alternative_component,add_or_exclude_per_definition,source,"
        "magnitude_only,not_applicable,blocked_primary_source_missing,"
        "primary source missing,notes\n"
        "BR_BANK_SPECIAL_SENSITIVITY,bank_special_regime_sensitivity,"
        "bank_special_regime_pension_obligations,sensitivity_component,"
        "separate_sensitivity,source,sensitivity_only,separate_sensitivity,"
        "blocked_primary_source_missing,primary source missing,notes\n",
        encoding="utf-8",
    )

    errors = validate_combined_balance_replication(replication, bridge)
    assert "Blocked combined-balance row must not contain value on row 2" in errors


def test_joint_balance_definitions_require_core_perimeters(tmp_path: Path) -> None:
    definitions = tmp_path / "joint_balance_definitions.csv"
    rules = tmp_path / "joint_balance_definition_rules.csv"
    definitions.write_text(
        "definition_id,definition_label,definition_role,period,unit,accounting_basis,"
        "perimeter,inclusion_rule_ids,exclusion_rule_ids,consolidation_rule,"
        "bank_special_regime_treatment,historical_adjustment_policy,source_requirements,"
        "status,blocking_issue,notes\n"
        "RGSS_PREVIDENTIAL_REPORTED,reported,bad_role,2006-2025,EUR_million,basis,"
        "perimeter,INC_PREVIDENTIAL_BALANCE,EXC_CGA_BALANCE,no_consolidation,"
        "separate_not_included,reported,source,blocked_primary_source_missing,"
        "primary source missing,notes\n",
        encoding="utf-8",
    )
    rules.write_text(
        "rule_id,rule_type,component,operation,sign_convention,double_counting_guard,"
        "unit_requirement,source_requirement,status,blocking_issue,notes\n"
        "INC_PREVIDENTIAL_BALANCE,inclusion,previdential_balance,add,"
        "positive_surplus_negative_deficit,guard,EUR_million,source,"
        "blocked_primary_source_missing,primary source missing,notes\n"
        "EXC_CGA_BALANCE,exclusion,cga_balance,exclude,not_applicable,guard,"
        "EUR_million,source,blocked_primary_source_missing,primary source missing,notes\n",
        encoding="utf-8",
    )

    errors = validate_joint_balance_definitions(definitions, rules)
    assert "Missing joint balance definition: CGA_INSTITUTIONAL_BALANCE" in errors
    assert "Missing joint balance rule: INC_CGA_BALANCE" in errors
    assert "Unexpected joint balance definition_role on row 2" in errors


def test_joint_balance_rules_require_double_counting_guards(tmp_path: Path) -> None:
    definitions = tmp_path / "joint_balance_definitions.csv"
    rules = tmp_path / "joint_balance_definition_rules.csv"
    definitions.write_text(
        "definition_id,definition_label,definition_role,period,unit,accounting_basis,"
        "perimeter,inclusion_rule_ids,exclusion_rule_ids,consolidation_rule,"
        "bank_special_regime_treatment,historical_adjustment_policy,source_requirements,"
        "status,blocking_issue,notes\n"
        "RGSS_PREVIDENTIAL_REPORTED,reported RGSS previdential balance,base_perimeter,"
        "2006-2025,EUR_million,basis,perimeter,INC_PREVIDENTIAL_BALANCE,"
        "EXC_CGA_BALANCE,none,separate_not_included,reported,source,"
        "blocked_primary_source_missing,primary source missing,notes\n"
        "CGA_INSTITUTIONAL_BALANCE,CGA institutional balance,base_perimeter,2006-2025,"
        "EUR_million,basis,perimeter,INC_CGA_BALANCE,EXC_PREVIDENTIAL_BALANCE,none,"
        "separate_not_included,reported,source,blocked_primary_source_missing,"
        "primary source missing,notes\n"
        "SIMPLE_CGA_PREVIDENTIAL_COMBINED,simple combined,combined_perimeter,"
        "2006-2025,EUR_million,basis,perimeter,INC_CGA_BALANCE;INC_PREVIDENTIAL_BALANCE,"
        "EXC_FEFSS_STOCK;EXC_BANK_SPECIAL_OBLIGATIONS,none,separate_not_included,"
        "reported,source,blocked_primary_source_missing,primary source missing,notes\n"
        "CONSOLIDATED_GENERAL_GOVERNMENT,consolidated,consolidated_perimeter,"
        "2006-2025,EUR_million,basis,perimeter,INC_CONSOLIDATION_ELIMINATIONS,"
        "EXC_INTRA_PUBLIC_TRANSFERS,eliminate_transfers,separate_visible_sensitivity,"
        "reported,source,blocked_primary_source_missing,primary source missing,notes\n"
        "HISTORICALLY_ADJUSTED_WORKING_GROUP,adjusted,historical_adjustment_variant,"
        "2006-2025,EUR_million,basis,perimeter,INC_HISTORICAL_ADJUSTMENTS,"
        "EXC_FEFSS_STOCK,adjust_only_with_registered_bridge,separate_not_included,"
        "adjusted,source,blocked_primary_source_missing,primary source missing,notes\n"
        "HISTORICALLY_ADJUSTED_NO_EARLY_RETIREMENT,no early retirement,"
        "historical_adjustment_variant,2006-2025,EUR_million,basis,perimeter,"
        "INC_CGA_BALANCE,EXC_EARLY_RETIREMENT_ADJUSTMENT,"
        "adjust_only_with_registered_bridge,separate_not_included,adjusted,source,"
        "blocked_primary_source_missing,primary source missing,notes\n"
        "FEFSS_VISIBLE_ALTERNATIVE,FEFSS visible,alternative_perimeter,2006-2025,"
        "EUR_million,basis,perimeter,INC_FEFSS_FLOW,EXC_FEFSS_STOCK,none,"
        "separate_not_included,reported,source,blocked_primary_source_missing,"
        "primary source missing,notes\n"
        "BANK_SPECIAL_SEPARATE_SENSITIVITY,bank sensitivity,sensitivity_perimeter,"
        "2006-2025,EUR_million,basis,perimeter,INC_BANK_SPECIAL_OBLIGATIONS,"
        "EXC_FEFSS_STOCK,none,separate_visible_sensitivity,reported,source,"
        "blocked_primary_source_missing,primary source missing,notes\n",
        encoding="utf-8",
    )
    rules.write_text(
        "rule_id,rule_type,component,operation,sign_convention,double_counting_guard,"
        "unit_requirement,source_requirement,status,blocking_issue,notes\n"
        "INC_PREVIDENTIAL_BALANCE,inclusion,previdential_balance,add,sign,,"
        "EUR_million,source,blocked_primary_source_missing,primary source missing,notes\n"
        "INC_CGA_BALANCE,inclusion,cga_balance,add,sign,guard,EUR_million,source,"
        "blocked_primary_source_missing,primary source missing,notes\n"
        "INC_CONSOLIDATION_ELIMINATIONS,inclusion,consolidation,adjust,sign,guard,"
        "EUR_million,source,blocked_primary_source_missing,primary source missing,notes\n"
        "INC_HISTORICAL_ADJUSTMENTS,inclusion,historical,adjust,sign,guard,"
        "EUR_million,source,blocked_primary_source_missing,primary source missing,notes\n"
        "INC_FEFSS_FLOW,inclusion,fefss,add,sign,guard,EUR_million,source,"
        "blocked_primary_source_missing,primary source missing,notes\n"
        "INC_BANK_SPECIAL_OBLIGATIONS,inclusion,bank,show,sign,guard,EUR_million,source,"
        "blocked_primary_source_missing,primary source missing,notes\n"
        "EXC_CGA_BALANCE,exclusion,cga,exclude,sign,guard,EUR_million,source,"
        "blocked_primary_source_missing,primary source missing,notes\n"
        "EXC_PREVIDENTIAL_BALANCE,exclusion,previdential,exclude,sign,guard,"
        "EUR_million,source,blocked_primary_source_missing,primary source missing,notes\n"
        "EXC_FEFSS_STOCK,exclusion,fefss_stock,exclude,sign,guard,EUR_million,source,"
        "blocked_primary_source_missing,primary source missing,notes\n"
        "EXC_BANK_SPECIAL_OBLIGATIONS,exclusion,bank,exclude,sign,guard,EUR_million,"
        "source,blocked_primary_source_missing,primary source missing,notes\n"
        "EXC_INTRA_PUBLIC_TRANSFERS,exclusion,transfers,eliminate,sign,guard,"
        "EUR_million,source,blocked_primary_source_missing,primary source missing,notes\n"
        "EXC_EARLY_RETIREMENT_ADJUSTMENT,exclusion,early_retirement,exclude,sign,guard,"
        "EUR_million,source,blocked_primary_source_missing,primary source missing,notes\n",
        encoding="utf-8",
    )

    errors = validate_joint_balance_definitions(definitions, rules)
    assert "Missing double-counting guard on joint balance rule row 2" in errors


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


def test_publication_artifact_readiness_blocks_unsupported_outputs(tmp_path: Path) -> None:
    companion_dir = tmp_path / "paper" / "figures" / "data"
    companion_dir.mkdir(parents=True)
    for filename in ("fig01.csv", "fig02.csv"):
        (companion_dir / filename).write_text("artifact_id,status\nFIG,blocked\n", encoding="utf-8")
    readiness = tmp_path / "publication_artifact_readiness_requirements.csv"
    readiness.write_text(
        "artifact_id,artifact_type,publication_status,companion_csv,required_inputs,"
        "available_inputs,permitted_use,status,blocking_issue,notes\n"
        "FIG01,figure,ready_partial,paper/figures/data/fig01.csv,inputs,observed,"
        "ready_article_use,ready_bounded,missing records,partial\n"
        "FIG02,figure,blocked,paper/figures/data/fig02.csv,inputs,observed,"
        "bounded_article_use,ready_bounded,missing records,notes\n"
        "TAB01,figure,ready,paper/figures/data/fig01.csv,inputs,observed,"
        "ready_article_use,ready_partial_bounded,none,notes\n"
        "TAB02,table,ready,paper/figures/data/fig02.csv,inputs,observed,"
        "bounded_article_use,ready_bounded,none,notes\n",
        encoding="utf-8",
    )

    errors = validate_publication_artifact_readiness(readiness, tmp_path)
    assert "Missing publication artifact readiness row: FIG03" in errors
    assert "Partial artifact FIG01 must be bounded article use" in errors
    assert "Partial artifact FIG01 must use bounded readiness status" in errors
    assert "Partial artifact FIG01 must name missing primary inputs" in errors
    assert "Partial artifact FIG01 must state its boundary" in errors
    assert "Blocked artifact FIG02 must block article use" in errors
    assert "Blocked artifact FIG02 must use blocked readiness status" in errors
    assert "Blocked artifact FIG02 must name missing primary inputs" in errors
    assert "Blocked artifact FIG02 must not claim available inputs" in errors
    assert "Ready artifact TAB01 must be a table in this release" in errors
    assert "Ready artifact TAB01 must remain bounded article use" in errors
    assert "Ready artifact TAB01 must use ready_bounded status" in errors


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


def test_falsification_decision_requirements_block_overclaims(tmp_path: Path) -> None:
    decisions = tmp_path / "falsification_decision_requirements.csv"
    decisions.write_text(
        "requirement_id,test_id,claim_boundary,required_inputs,current_status,"
        "permitted_language,blocked_language,status,blocking_issue,notes\n"
        "R1,FALS_001,remittance,withholding,current,claim,gap,"
        "blocked_requires_sources,missing records,notes\n"
        "R2,FALS_002,employer,rates,current,claim,gap,"
        "partial_bounded_review,missing records,notes\n"
        "R3,FALS_003,state,inputs,current,claim,conclusion,"
        "blocked_requires_sources,missing primary records,notes\n"
        "R4,FALS_004,rgss,inputs,current,claim,conclusion,"
        "blocked_requires_sources,missing primary records,notes\n"
        "R5,FALS_005,balance,inputs,current,claim,deficit,"
        "blocked_requires_sources,missing primary records,notes\n"
        "R6,FALS_006,bank,inputs,current,identity,claim,"
        "partial_bounded_review,missing records,notes\n"
        "R7,FALS_007,discount,inputs,current,claim,adverse,"
        "blocked_requires_sources,missing primary records,notes\n"
        "R8,FALS_008,lifecycle,inputs,current,claim,adverse,"
        "blocked_requires_sources,missing primary records,notes\n"
        "R9,ALL,gate,inputs,current,claim,claim,"
        "partial_bounded_review,none,notes\n",
        encoding="utf-8",
    )

    errors = validate_falsification_decision_requirements(decisions)
    assert "Blocked falsification decisions must name missing primary inputs on row 2" in errors
    assert "FALS_001 decision must block remittance-gap claims" in errors
    assert "FALS_002 decision must block quantified employer-gap claims" in errors
    assert "FALS_003 decision must block State financing-intent claims" in errors
    assert "FALS_004 decision must block RGSS magnitude claims" in errors
    assert "FALS_005 decision must block combined-balance sign claims" in errors
    assert (
        "FALS_006 decision must allow only the 2012 identity and block lifecycle claims" in errors
    )
    assert "FALS_007 decision must block selected-discount-rate claims" in errors
    assert "FALS_008 decision must block lifecycle classification claims" in errors
    assert (
        "Overall falsification manuscript gate must permit only bounded source-backed language"
    ) in errors


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
