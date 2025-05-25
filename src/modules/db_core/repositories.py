from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select, insert

from ...db.base_repository import BaseRepository
from ...db.tables import table_schemas_table, table_definitions_table, table_columns_table
from . import models


class SchemasRepository(BaseRepository):
    def __init__(self, conn: AsyncConnection):
        super().__init__(conn)
    
    async def create(self, data: models.SchemaCreate) -> models.Schema:
        stmt = insert(table_schemas_table).values(**data.dict()).returning(table_schemas_table.c.id)
        result = await self.connection.execute(stmt)
        schema_id = result.scalar_one()
        return models.Schema(**data.model_dump(), id=schema_id)
    
    async def update(self, schema_id: int, data: models.SchemaUpdate) -> models.Schema:
        stmt = (
            table_schemas_table.update()
            .where(table_schemas_table.c.id == schema_id)
            .values(**data.dict())
        )
        await self.connection.execute(stmt)
        return models.Schema(**data.dict(), id=schema_id)

    async def get_all(self) -> list[models.Schema]:
        stmt = select(table_schemas_table)
        result = await self.connection.execute(stmt)
        rows = result.fetchall()
        return [models.Schema(**row._mapping) for row in rows]

class TableRepository(BaseRepository):
    def __init__(self, conn: AsyncConnection):
        super().__init__(conn)
    
    async def create(self, data: models.TableCreate) -> models.Table:
        stmt = insert(table_definitions_table).values(**data.dict()).returning(table_definitions_table.c.id)
        result = await self.connection.execute(stmt)
        table_id = result.scalar_one()
        return models.Table(**data.dict(), id=table_id)
    
    async def update(self, table_id: int, data: models.TableUpdate) -> models.Table:
        stmt = (
            table_definitions_table.update()
            .where(table_definitions_table.c.id == table_id)
            .values(**data.dict())
        )
        await self.connection.execute(stmt)
        return models.Table(**data.dict(), id=table_id)
    
    async def get_all(self) -> list[models.Table]:
        stmt = select(table_definitions_table)
        result = await self.connection.execute(stmt)
        rows = result.fetchall()
        return [models.Table(**row._mapping) for row in rows]

class TableColumnRepository(BaseRepository):
    def __init__(self, conn: AsyncConnection):
        super().__init__(conn)
    
    async def create(self, data: models.Column) -> models.Column:
        stmt = insert(table_columns_table).values(**data.dict()).returning(table_columns_table.c.id)
        result = await self.connection.execute(stmt)
        column_id = result.scalar_one()
        return models.Column(**data.dict(), id=column_id)
    
    async def update(self, column_id: int, data: models.ColumnUpdate) -> models.Column:
        stmt = (
            table_columns_table.update()
            .where(table_columns_table.c.id == column_id)
            .values(**data.dict())
        )
        await self.connection.execute(stmt)
        return models.Column(**data.dict(), id=column_id)
    
    async def get_all(self) -> list[models.Column]:
        stmt = select(table_columns_table)
        result = await self.connection.execute(stmt)
        rows = result.fetchall()
        return [models.Column(**row._mapping) for row in rows]

