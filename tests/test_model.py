import pytest

from star_schema_builder.model import Column, ColumnRole, build_star_schema


def test_builds_dimensions_and_fact_from_flat_columns():
    columns = [
        Column("invoice_number", ColumnRole.DEGENERATE, sql_type="TEXT"),
        Column("client_name", ColumnRole.DIMENSION_ATTRIBUTE, dimension="client", sql_type="TEXT"),
        Column("client_document", ColumnRole.DIMENSION_ATTRIBUTE, dimension="client", sql_type="TEXT"),
        Column("branch_name", ColumnRole.DIMENSION_ATTRIBUTE, dimension="branch", sql_type="TEXT"),
        Column("total_amount", ColumnRole.MEASURE, sql_type="NUMERIC(12,2)"),
    ]

    schema = build_star_schema("billing", columns)

    assert schema.fact.name == "fact_billing"
    assert {dim.name for dim in schema.dimensions.values()} == {"dim_client", "dim_branch"}
    assert len(schema.dimensions["client"].attributes) == 2
    assert schema.fact.dimension_keys == ["dim_client_key", "dim_branch_key"] or set(
        schema.fact.dimension_keys
    ) == {"dim_client_key", "dim_branch_key"}


def test_requires_at_least_one_measure():
    columns = [Column("client_name", ColumnRole.DIMENSION_ATTRIBUTE, dimension="client")]
    with pytest.raises(ValueError):
        build_star_schema("billing", columns)


def test_dimension_attribute_requires_dimension_name():
    with pytest.raises(ValueError):
        Column("client_name", ColumnRole.DIMENSION_ATTRIBUTE)
