from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
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
