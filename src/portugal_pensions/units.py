"""Unit, currency, price-basis, and timing compatibility utilities."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

import pandas as pd

ESCUDOS_PER_EURO = Decimal("200.482")


class UnitCompatibilityError(ValueError):
    """Raised when two series cannot be joined without an explicit conversion."""


@dataclass(frozen=True)
class UnitDefinition:
    """Definition of a unit registry row."""

    unit_id: str
    currency: str
    scale: str
    price_basis: str
    base_year: str
    flow_or_stock: str
    accounting_basis: str
    conversion_rule: str
    valid_from: str
    valid_to: str
    canonical_unit: str
    join_family: str
    notes: str


@dataclass(frozen=True)
class SeriesMetadata:
    """Metadata required before joining numeric series."""

    unit: str
    currency: str
    price_basis: str
    accounting_basis: str
    flow_or_stock: str
    time_reference: str


def escudos_to_euros(value: Decimal | int | str) -> Decimal:
    """Convert Portuguese escudos to euros using the official fixed rate."""
    return Decimal(value) / ESCUDOS_PER_EURO


def load_unit_registry(path: Path) -> dict[str, UnitDefinition]:
    """Load the unit registry keyed by unit_id."""
    if not isinstance(path, Path):
        raise TypeError("path must be pathlib.Path")
    rows = pd.read_csv(path, dtype=str, keep_default_na=False)
    definitions: dict[str, UnitDefinition] = {}
    for row in rows.to_dict("records"):
        unit_id = str(row["unit_id"])
        if not unit_id:
            continue
        definitions[unit_id] = UnitDefinition(
            unit_id=unit_id,
            currency=str(row["currency"]),
            scale=str(row["scale"]),
            price_basis=str(row["price_basis"]),
            base_year=str(row["base_year"]),
            flow_or_stock=str(row["flow_or_stock"]),
            accounting_basis=str(row["accounting_basis"]),
            conversion_rule=str(row["conversion_rule"]),
            valid_from=str(row["valid_from"]),
            valid_to=str(row["valid_to"]),
            canonical_unit=str(row["canonical_unit"]),
            join_family=str(row["join_family"]),
            notes=str(row["notes"]),
        )
    return definitions


def assert_compatible_for_join(left: SeriesMetadata, right: SeriesMetadata) -> None:
    """Fail if two series cannot be joined without an explicit conversion."""
    mismatches = []
    for field in (
        "unit",
        "currency",
        "price_basis",
        "accounting_basis",
        "flow_or_stock",
        "time_reference",
    ):
        if getattr(left, field) != getattr(right, field):
            mismatches.append(field)
    if mismatches:
        raise UnitCompatibilityError(
            "Incompatible series metadata for join: " + ", ".join(mismatches)
        )


def canonicalize_unit_value(value: Decimal | int | str, unit: UnitDefinition) -> Decimal:
    """Convert a numeric value to the row's canonical unit when a rule exists."""
    numeric = Decimal(value)
    if unit.conversion_rule == "none":
        return numeric
    if unit.conversion_rule == "fixed_escudo_euro_200_482":
        return escudos_to_euros(numeric)
    if unit.conversion_rule == "divide_by_100_for_rate":
        return numeric / Decimal("100")
    raise UnitCompatibilityError(f"Unsupported conversion rule: {unit.conversion_rule}")
