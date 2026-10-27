"""star_schema_builder

Turns a flat operational table description into a dimensional model
(Kimball-style star schema): fact table DDL + dimension table DDL,
inferred from a simple column classification you provide.

Useful for the recurring "we have a flat billing/operations table, we
need a proper fact/dimension model for BI" migration.
"""

from .ddl import generate_ddl
from .model import Column, ColumnRole, StarSchema, build_star_schema

__all__ = ["Column", "ColumnRole", "StarSchema", "build_star_schema", "generate_ddl"]
__version__ = "0.1.0"
