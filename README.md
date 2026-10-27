# star-schema-builder

Turns the description of a flat operational table into a Kimball-style star schema. You classify each column once (measure, dimension attribute or degenerate dimension) and it builds the fact and dimension tables and prints the `CREATE TABLE` statements.

I wrote it for a situation that keeps coming back in BI work: a dashboard reads from one wide billing or operations table, and at some point that table needs to become a proper fact/dimension model.

## Usage

```python
from star_schema_builder import Column, ColumnRole, build_star_schema, generate_ddl

columns = [
    Column("invoice_number", ColumnRole.DEGENERATE, sql_type="TEXT"),
    Column("client_name", ColumnRole.DIMENSION_ATTRIBUTE, dimension="client", sql_type="TEXT"),
    Column("client_document", ColumnRole.DIMENSION_ATTRIBUTE, dimension="client", sql_type="TEXT"),
    Column("branch_name", ColumnRole.DIMENSION_ATTRIBUTE, dimension="branch", sql_type="TEXT"),
    Column("total_amount", ColumnRole.MEASURE, sql_type="NUMERIC(12,2)"),
]

schema = build_star_schema("billing", columns)
print(generate_ddl(schema))
```

Output:

```sql
CREATE TABLE dim_client (
    dim_client_key SERIAL PRIMARY KEY,
    client_name TEXT,
    client_document TEXT
);

CREATE TABLE dim_branch (
    dim_branch_key SERIAL PRIMARY KEY,
    branch_name TEXT
);

CREATE TABLE fact_billing (
    fact_id BIGSERIAL PRIMARY KEY,
    dim_client_key INTEGER REFERENCES dim_client(dim_client_key),
    dim_branch_key INTEGER REFERENCES dim_branch(dim_branch_key),
    invoice_number TEXT,
    total_amount NUMERIC(12,2)
);
```

The DDL targets PostgreSQL (`SERIAL`, `BIGSERIAL`).

## Development

```bash
pip install pytest ruff
pytest
ruff check .
```

## License

MIT, see [LICENSE](LICENSE).
