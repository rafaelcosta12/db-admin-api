from typing import List, Optional
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from .. import models
from ....db.tables import users_table
from ....db.base_repository import BaseRepository


class UsersRepository(BaseRepository):
    def __init__(self, conn: AsyncConnection):
        super().__init__(conn)

    async def list(self) -> List[models.User]:
        stmt = select(users_table)
        result = await self.connection.execute(stmt)
        return [models.User(**i._mapping) for i in result.fetchall()]
    
    async def find(self, id: Optional[int] = None, email: Optional[str] = None) -> models.User | None:
        stmt = select(users_table)
        
        if id:
            stmt = stmt.where(users_table.c.id == id)
        
        if email:
            stmt = stmt.where(users_table.c.email == email)
        
        result = (await self.connection.execute(stmt)).fetchone()
        
        if result:
            return models.User(**result._mapping)
        
        return None

    async def insert(self, data: models.UserCreate) -> Optional[int]:
        stmt = (
            insert(users_table)
                .values(**data.model_dump())
                .returning(users_table.c.id)
        )
        result = await self.connection.execute(stmt)
        return result.scalar()

    async def update(self, user_id: int, data: models.UserUpdate) -> None:
        stmt = (
            users_table.update()
                .where(users_table.c.id == user_id)
                .values(**data.model_dump(exclude_unset=True))
        )
        await self.connection.execute(stmt)
