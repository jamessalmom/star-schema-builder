"""Domain model: classify flat columns into measures/dimension attributes,
then group dimension attributes into dimension tables by declared grain.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ColumnRole(str, Enum):
    MEASURE = "measure"
    DIMENSION_ATTRIBUTE = "dimension_attribute"
    DEGENERATE = "degenerate"  # stays on the fact table (e.g. invoice number)


@dataclass(frozen=True)
class Column:
    name: str
    role: ColumnRole
    dimension: str | None = None  # required when role == DIMENSION_ATTRIBUTE
    sql_type: str = "TEXT"

    def __post_init__(self) -> None:
        if self.role == ColumnRole.DIMENSION_ATTRIBUTE and not self.dimension:
            raise ValueError(f"column '{self.name}' needs a dimension name")


@dataclass
class DimensionTable:
    name: str
    attributes: list[Column] = field(default_factory=list)

    @property
    def surrogate_key(self) -> str:
        return f"{self.name}_key"


@dataclass
class FactTable:
    name: str
    measures: list[Column]
    degenerate_dimensions: list[Column]
    dimension_keys: list[str]


@dataclass
class StarSchema:
    fact: FactTable
    dimensions: dict[str, DimensionTable]


def build_star_schema(source_table: str, columns: list[Column]) -> StarSchema:
    dimensions: dict[str, DimensionTable] = {}
    measures: list[Column] = []
    degenerate: list[Column] = []

    for col in columns:
        if col.role == ColumnRole.MEASURE:
            measures.append(col)
        elif col.role == ColumnRole.DEGENERATE:
            degenerate.append(col)
        else:
            dim = dimensions.setdefault(col.dimension, DimensionTable(name=f"dim_{col.dimension}"))
            dim.attributes.append(col)

    if not measures:
        raise ValueError("a star schema needs at least one measure column")

    fact = FactTable(
        name=f"fact_{source_table}",
        measures=measures,
        degenerate_dimensions=degenerate,
        dimension_keys=[dim.surrogate_key for dim in dimensions.values()],
    )
    return StarSchema(fact=fact, dimensions=dimensions)
