from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint, JSON
from datetime import datetime, timezone

metadata_obj = MetaData()

def now():
    return datetime.now(timezone.utc)

users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(128), nullable=False),
    Column("email", String(128), nullable=False),
    Column("password", String(256), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, default=now),
    Column("updated_at", DateTime(timezone=True), nullable=False, default=now, onupdate=now),
    Column("is_admin", Boolean, nullable=False, default=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("profile_img", String, nullable=True),
)

user_groups_table = Table(
    "user_groups",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(128), nullable=False, unique=True),
    Column("created_at", DateTime(timezone=True), nullable=False, default=now),
    Column("updated_at", DateTime(timezone=True), nullable=False, default=now, onupdate=now),
)

user_group_membership_table = Table(
    "user_group_membership",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("group_id", Integer, ForeignKey("user_groups.id", ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, default=now),
    Column("updated_at", DateTime(timezone=True), nullable=False, default=now, onupdate=now),
    UniqueConstraint("user_id", "group_id", name="uq_user_group_membership")
)

table_schemas_table = Table(
    "table_schemas",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(128), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, default=now),
    Column("updated_at", DateTime(timezone=True), nullable=False, default=now, onupdate=now),
    Column("comment", String(256), nullable=True),
)

table_definitions_table = Table(
    "table_definitions",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("table_schema_id", Integer, ForeignKey("table_schemas.id"), nullable=False),
    Column("name", String(128), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, default=now),
    Column("updated_at", DateTime(timezone=True), nullable=False, default=now, onupdate=now),
    Column("comment", String(256), nullable=True),
    UniqueConstraint("table_schema_id", "name", name="uq_table_definitions"),
)

table_columns_table = Table(
    "table_columns",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("table_id", Integer, ForeignKey("table_definitions.id"), nullable=False),
    Column("name", String(128), nullable=False),
    Column("type", String(128), nullable=False),
    Column("nullable", Boolean, nullable=False, default=True),
    Column("default", String(256), nullable=True),
    Column("autoincrement", Boolean, nullable=False, default=False),
    Column("comment", String(256), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False, default=now),
    Column("updated_at", DateTime(timezone=True), nullable=False, default=now, onupdate=now),
    UniqueConstraint("table_id", "name", name="uq_table_columns"),
)