from sqlalchemy import select, insert, func, Select
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.exc import IntegrityError

from ....db.base_repository import BaseRepository
from ....db.tables import user_groups_table, user_group_membership_table, users_table
from .. import models


class GroupExistsError(Exception):
    """Exception raised when a user group with the same name already exists."""
    pass

class OperationFailedError(Exception):
    """Exception raised when an operation fails."""
    pass


class UsersGroupRepository(BaseRepository):
    def __init__(self, conn: AsyncConnection):
        super().__init__(conn)
    
    async def list_by_filter(self, filter: models.UserGroupSearchFilter) -> models.PaginationSearchResult[models.UserGroup]:
        stmt = self._apply_filters(select(user_groups_table), filter)
        
        if filter.limit:
            stmt = stmt.limit(filter.limit)
        if filter.offset:
            stmt = stmt.offset(filter.offset)
        if filter.order_by:
            if filter.order == "asc":
                stmt = stmt.order_by(getattr(user_groups_table.c, filter.order_by).asc())
            else:
                stmt = stmt.order_by(getattr(user_groups_table.c, filter.order_by).desc())

        results = await self.connection.execute(stmt)

        stmt = self._apply_filters(select(func.count(user_groups_table.c.id)), filter)
        count = await self.connection.execute(stmt)
        
        return models.PaginationSearchResult(
            items=[models.UserGroup(**i._mapping) for i in results.fetchall()],
            total=count.scalar_one(),
            page=filter.offset // filter.limit + 1 if filter.limit else 1,
        )

    def _apply_filters(self, stmt: Select, filter: models.UserGroupSearchFilter) -> Select:
        if filter.text:
            stmt = stmt.where(
                (user_groups_table.c.name.ilike(f"%{filter.text}%"))
            )
        if filter.name:
            stmt = stmt.where(user_groups_table.c.name.ilike(f"%{filter.name}%"))
        
        return stmt

    async def list_user_counts_by_group(self, group_ids: list[int]) -> list[models.UserCountByGroup]:
        stmt = (
            select(
                user_group_membership_table.c.group_id,
                func.count(user_group_membership_table.c.user_id).label("user_count")
            )
            .where(user_group_membership_table.c.group_id.in_(group_ids))
            .group_by(user_group_membership_table.c.group_id)
        )
        result = await self.connection.execute(stmt)
        return [models.UserCountByGroup(**row._mapping) for row in result.fetchall()]

    async def create(self, user_group: models.UserGroupCreate) -> int:
        stmt = (
            insert(user_groups_table)
                .values(**user_group.dict())
                .returning(user_groups_table.c.id)
        )
        try:
            result = await self.connection.execute(stmt)
            user_group_id = result.scalar_one()
            if not user_group_id:
                raise Exception("Failed to create user group")
            return user_group_id
        except IntegrityError:
            raise GroupExistsError(f"User group with name {user_group.name} already exists")

    async def find(self, id: int) -> models.UserGroup | None:
        stmt = (
            select(user_groups_table)
                .where(user_groups_table.c.id == id)
        )
        result = await self.connection.execute(stmt)
        row = result.fetchone()
        if row:
            return models.UserGroup(**row._mapping)
        return None
    
    async def update(self, id: int, user_group: models.UserGroupUpdate) -> bool:
        try:
            stmt = (
                user_groups_table.update()
                    .where(user_groups_table.c.id == id)
                    .values(**user_group.dict(exclude_unset=True))
            )
            result = await self.connection.execute(stmt)
            return result.rowcount > 0
        except IntegrityError:
            raise GroupExistsError(f"User group with name {user_group.name} already exists")
    
    async def delete(self, id: int) -> bool:
        stmt = (
            user_groups_table.delete()
                .where(user_groups_table.c.id == id)
        )
        result = await self.connection.execute(stmt)
        return result.rowcount > 0

    async def add_user_to_group(self, group_id: int, user_id: int) -> bool:
        try:
            stmt = (
                insert(user_group_membership_table)
                    .values(user_id=user_id, group_id=group_id)
            )
            await self.connection.execute(stmt)
            return True
        except IntegrityError as e:
            raise OperationFailedError(f"Failed to add user {user_id} to group {group_id}") from e

    async def remove_user_from_group(self, group_id: int, user_id: int):
        stmt = (
            user_group_membership_table.delete()
                .where(user_group_membership_table.c.group_id == group_id)
                .where(user_group_membership_table.c.user_id == user_id)
        )
        await self.connection.execute(stmt)
    
    async def list_users_in_group(self, group_id: int) -> list[models.User]:
        stmt = (
            select(users_table.join(user_group_membership_table))
                .where(user_group_membership_table.c.group_id == group_id)
        )
        result = await self.connection.execute(stmt)
        return [models.User(**i._mapping) for i in result.fetchall()]
