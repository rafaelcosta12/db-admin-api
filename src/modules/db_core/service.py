from .repositories import SchemasRepository, TableRepository, TableColumnRepository
from . import models

class DbCoreService:
    def __init__(self, schemas_repository: SchemasRepository,  tables_repository: TableRepository, column_repository: TableColumnRepository):
        self.schemas_repository = schemas_repository
        self.tables_repository = tables_repository
        self.column_repository = column_repository
    
    async def update_schemas(self, schemas: list[models.SchemaCreate]) -> list[models.Schema]:
        all_db_schemas = {schema.name:schema for schema in await self.schemas_repository.get_all()}
        updated_schemas: list[models.Schema] = []

        for schema in schemas:
            if schema.name in ["information_schema"]:
                continue
            if schema.name in all_db_schemas:
                db_schema = all_db_schemas[schema.name]
                item = await self.schemas_repository.update(db_schema.id, models.SchemaUpdate(**schema.dict()))
            else:
                item = await self.schemas_repository.create(schema)
            updated_schemas.append(item)
        
        return updated_schemas

    async def update_tables(self, tables: list[models.TableCreate]):
        all_db_tables = {table.name:table for table in await self.tables_repository.get_all()}
        updated_tables: list[models.Table] = []
        
        for table in tables:
            if table.name in all_db_tables:
                db_table = all_db_tables[table.name]
                item = await self.tables_repository.update(db_table.id, models.TableUpdate(**table.dict()))
            else:
                item = await self.tables_repository.create(table)
            updated_tables.append(item)
        
        return updated_tables
    
    async def update_columns(self, columns: list[models.Column]):
        all_db_columns = {column.name:column for column in await self.column_repository.get_all()}
        updated_columns: list[models.Column] = []
        
        for column in columns:
            if column.name in all_db_columns:
                db_column = all_db_columns[column.name]
                item = await self.column_repository.update(db_column.id, models.ColumnUpdate(**column.dict()))
            else:
                item = await self.column_repository.create(column)
            updated_columns.append(item)
        
        return updated_columns