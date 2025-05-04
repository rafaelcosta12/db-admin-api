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
        return models.Schema(**data.dict(), id=schema_id)
    
    async def update(self, schema_id: int, data: models.SchemaUpdate) -> None:
        stmt = (
            table_schemas_table.update()
            .where(table_schemas_table.c.id == schema_id)
            .values(**data.dict())
        )
        await self.connection.execute(stmt)

    async def delete(self, schema_id: int) -> None:
        stmt = table_schemas_table.delete().where(table_schemas_table.c.id == schema_id)
        await self.connection.execute(stmt)
    
    async def find(self, schema_id: int) -> models.Schema:
        stmt = select(table_schemas_table).where(table_schemas_table.c.id == schema_id)
        result = await self.connection.execute(stmt)
        row = result.fetchone()
        if not row:
            raise models.SchemaNotFoundError(f"Schema with id {schema_id} not found.")
        else:
            return models.Schema(**row._mapping)

    async def all(self) -> list[models.Schema]:
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

class TableColumnRepository(BaseRepository):
    def __init__(self, conn: AsyncConnection):
        super().__init__(conn)
    
    async def create(self, data: models.Column) -> models.Column:
        stmt = insert(table_columns_table).values(**data.dict()).returning(table_columns_table.c.id)
        result = await self.connection.execute(stmt)
        column_id = result.scalar_one()
        return models.Column(**data.dict(), id=column_id)
