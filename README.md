# star-schema-builder

Turns a flat operational table description into a **Kimball-style star
schema** (fact + dimension tables): you classify each column once
(measure / dimension attribute / degenerate), and it generates the
dimensional model and the `CREATE TABLE` DDL.

Built from the recurring migration of "we have a flat billing/operations
table feeding a management dashboard, we need a real fact/dimension model"
— the exact step taken when moving a BI portal off static exports and onto
a proper warehouse schema.

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

CREATE TABLE fact_billing (
    fact_id BIGSERIAL PRIMARY KEY,
    dim_client_key INTEGER REFERENCES dim_client(dim_client_key),
    invoice_number TEXT,
    total_amount NUMERIC(12,2)
);
```

## Development

```bash
pip install pytest ruff
pytest
ruff check .
```

## License

MIT — see [LICENSE](LICENSE).
