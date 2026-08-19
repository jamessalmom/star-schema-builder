"""Renders CREATE TABLE DDL for a StarSchema (ANSI-ish SQL, Postgres-friendly)."""

from __future__ import annotations

from .model import StarSchema


def _dimension_ddl(dim) -> str:
    lines = [f"CREATE TABLE {dim.name} (", f"    {dim.surrogate_key} SERIAL PRIMARY KEY,"]
    for attr in dim.attributes:
        lines.append(f"    {attr.name} {attr.sql_type},")
    lines[-1] = lines[-1].rstrip(",")
    lines.append(");")
    return "\n".join(lines)


def _fact_ddl(schema: StarSchema) -> str:
    fact = schema.fact
    lines = [f"CREATE TABLE {fact.name} (", "    fact_id BIGSERIAL PRIMARY KEY,"]
    for dim in schema.dimensions.values():
        lines.append(f"    {dim.surrogate_key} INTEGER REFERENCES {dim.name}({dim.surrogate_key}),")
    for deg in fact.degenerate_dimensions:
        lines.append(f"    {deg.name} {deg.sql_type},")
    for measure in fact.measures:
        lines.append(f"    {measure.name} {measure.sql_type},")
    lines[-1] = lines[-1].rstrip(",")
    lines.append(");")
    return "\n".join(lines)


def generate_ddl(schema: StarSchema) -> str:
    parts = [_dimension_ddl(dim) for dim in schema.dimensions.values()]
    parts.append(_fact_ddl(schema))
    return "\n\n".join(parts)
