import pytest

from portugal_pensions.extraction import (
    ExtractionRecord,
    normalize_extraction_text,
    parse_accounting_number,
)


def test_parse_accounting_number_accepts_portuguese_decimal() -> None:
    assert parse_accounting_number("1 234,56") == 1234.56


def test_parse_accounting_number_accepts_parenthesized_negative() -> None:
    assert parse_accounting_number("(290,6)") == -290.6


def test_parse_accounting_number_rejects_empty_text() -> None:
    with pytest.raises(ValueError, match="value is empty"):
        parse_accounting_number("  ")


def test_normalize_extraction_text_collapses_whitespace() -> None:
    assert normalize_extraction_text("CGA\n  186.2") == "CGA 186.2"


def test_extraction_record_exports_csv_row() -> None:
    record = ExtractionRecord(
        source_id="SRC",
        page="1",
        table_title="Table",
        row_label="Row",
        column_label="Column",
        original_text="value 1",
        parsed_value="1",
        unit="EUR_million",
        extraction_method="pdftotext",
        validation_method="checked",
        qa_tier="routine",
        secondary_check="not_required",
        parsing_warning="none",
        status="extracted",
        notes="notes",
    )

    assert record.as_csv_row()["source_id"] == "SRC"
