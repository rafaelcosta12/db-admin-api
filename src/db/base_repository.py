from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncConnection

class BaseRepository:
    def __init__(self, conn: AsyncConnection):
        self._conn = conn

    @property
    def connection(self) -> AsyncConnection:
        return self._conn

    async def execute(self, stmt):
        return await self._conn.execute(stmt)