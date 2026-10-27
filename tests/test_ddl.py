from star_schema_builder.ddl import generate_ddl
from star_schema_builder.model import Column, ColumnRole, build_star_schema


def test_generates_create_table_statements():
    columns = [
        Column("client_name", ColumnRole.DIMENSION_ATTRIBUTE, dimension="client", sql_type="TEXT"),
        Column("total_amount", ColumnRole.MEASURE, sql_type="NUMERIC(12,2)"),
    ]
    schema = build_star_schema("billing", columns)
    ddl = generate_ddl(schema)

    assert "CREATE TABLE dim_client" in ddl
    assert "CREATE TABLE fact_billing" in ddl
    assert "REFERENCES dim_client(dim_client_key)" in ddl
    assert "total_amount NUMERIC(12,2)" in ddl


def test_public_api_exports_column_role():
    import star_schema_builder

    assert hasattr(star_schema_builder, "ColumnRole")
    assert "ColumnRole" in star_schema_builder.__all__
