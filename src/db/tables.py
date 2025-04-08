from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from datetime import datetime, timezone

metadata_obj = MetaData()
now = lambda: datetime.now(timezone.utc)

users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(128), nullable=False),
    Column("email", String(128), nullable=False),
    Column("password", String(256), nullable=False),
    Column("created_at", DateTime, nullable=False, default=now),
    Column("updated_at", DateTime, nullable=False, default=now, onupdate=now),
    Column("is_admin", Boolean, nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
)
