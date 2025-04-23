from typing import Optional
from sqlalchemy import select, insert, func, Select
from sqlalchemy.ext.asyncio import AsyncConnection

from .. import models
from ....db.tables import users_table
from ....db.base_repository import BaseRepository


class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the database."""
    pass


class UsersRepository(BaseRepository):
    def __init__(self, conn: AsyncConnection):
        super().__init__(conn)

    async def list_by_filter(self, filter: models.UserSearchFilter) -> models.PaginationSearchResult[models.User]:
        stmt = self._apply_filters(select(users_table), filter)

        if filter.limit:
            stmt = stmt.limit(filter.limit)
        if filter.offset:
            stmt = stmt.offset(filter.offset)
        if filter.order_by:
            if filter.order == "asc":
                stmt = stmt.order_by(getattr(users_table.c, filter.order_by).asc())
            else:
                stmt = stmt.order_by(getattr(users_table.c, filter.order_by).desc())

        results = await self.connection.execute(stmt)
        
        stmt = self._apply_filters(select(func.count(users_table.c.id)), filter)
        count = await self.connection.execute(stmt)

        return models.PaginationSearchResult(
            items=[models.User(**i._mapping) for i in results.fetchall()],
            total=count.scalar_one(),
            page=filter.offset // filter.limit + 1 if filter.limit else 1,
        )
    
    def _apply_filters(self, stmt: Select, filter: models.UserSearchFilter) -> Select:
        if filter.text:
            stmt = stmt.where(
                (users_table.c.name.ilike(f"%{filter.text}%")) |
                (users_table.c.email.ilike(f"%{filter.text}%"))
            )
        if filter.name:
            stmt = stmt.where(users_table.c.name.ilike(f"%{filter.name}%"))
        if filter.email:
            stmt = stmt.where(users_table.c.email.ilike(f"%{filter.email}%"))
        if filter.is_admin is not None:
            stmt = stmt.where(users_table.c.is_admin == filter.is_admin)
        if filter.is_active is not None:
            stmt = stmt.where(users_table.c.is_active == filter.is_active)
        
        return stmt
    
    async def find(self, id: Optional[int] = None, email: Optional[str] = None) -> models.UserPassword | None:
        stmt = select(users_table)
        
        if id:
            stmt = stmt.where(users_table.c.id == id)
        
        if email:
            stmt = stmt.where(users_table.c.email == email)
        
        result = (await self.connection.execute(stmt)).fetchone()
        
        if result:
            return models.UserPassword(**result._mapping)
        
        return None

    async def insert(self, data: models.UserCreate) -> Optional[int]:
        stmt = (
            insert(users_table)
                .values(**data.model_dump())
                .returning(users_table.c.id)
        )
        result = await self.connection.execute(stmt)
        return result.scalar()

    async def update(self, user_id: int, data: models.UserUpdate) -> models.User:
        stmt = (
            users_table.update()
                .where(users_table.c.id == user_id)
                .values(**data.model_dump(exclude_unset=True))
        )
        await self.connection.execute(stmt)
        fresh = await self.find(id=user_id)
        
        if not fresh:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        return fresh

    async def delete(self, user_id: int) -> None:
        stmt = (
            users_table.delete()
                .where(users_table.c.id == user_id)
                .returning(users_table.c.id)
        )
        await self.connection.execute(stmt)