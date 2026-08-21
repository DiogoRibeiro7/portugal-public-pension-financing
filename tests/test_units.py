from decimal import Decimal
from pathlib import Path

import pytest

from portugal_pensions.units import (
    SeriesMetadata,
    UnitCompatibilityError,
    assert_compatible_for_join,
    canonicalize_unit_value,
    escudos_to_euros,
    load_unit_registry,
)


def test_escudos_to_euros_uses_fixed_rate() -> None:
    assert escudos_to_euros(Decimal("200.482")) == Decimal("1")


def test_join_metadata_accepts_identical_series() -> None:
    metadata = SeriesMetadata(
        unit="EUR_million",
        currency="EUR",
        price_basis="current_prices",
        accounting_basis="budgetary_public_accounts",
        flow_or_stock="flow",
        time_reference="accounting_year",
    )

    assert_compatible_for_join(metadata, metadata)


def test_join_metadata_rejects_accounting_basis_mismatch() -> None:
    left = SeriesMetadata(
        unit="EUR_million",
        currency="EUR",
        price_basis="current_prices",
        accounting_basis="budgetary_public_accounts",
        flow_or_stock="flow",
        time_reference="accounting_year",
    )
    right = SeriesMetadata(
        unit="EUR_million",
        currency="EUR",
        price_basis="current_prices",
        accounting_basis="ESA-2010_national_accounts",
        flow_or_stock="flow",
        time_reference="accounting_year",
    )

    with pytest.raises(UnitCompatibilityError, match="accounting_basis"):
        assert_compatible_for_join(left, right)


def test_unit_registry_loads_and_converts_escudos() -> None:
    root = Path(__file__).resolve().parents[1]
    registry = load_unit_registry(root / "evidence" / "unit_registry.csv")

    assert canonicalize_unit_value(Decimal("200.482"), registry["PTE_million"]) == Decimal("1")
