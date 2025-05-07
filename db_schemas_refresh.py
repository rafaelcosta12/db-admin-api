import asyncio
from sqlalchemy import create_engine, MetaData, inspect

from src.modules.db_core import models
from src.modules.db_core.repositories import SchemasRepository, TableRepository, TableColumnRepository
from src.modules.db_core.service import DbCoreService
from src.db.session import get_db_ctx

def get_data():
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/devstacker")
    connection = engine.connect()

    # Criar objeto de metadados
    metadata = MetaData()

    # Refletir todas as tabelas do banco de dados
    metadata.reflect(bind=engine)

    # Criar inspetor para obter informações detalhadas
    yield engine
    
    connection.close()
    engine.dispose()

def get_schemas():
    engine = next(get_data())
    inspector = inspect(engine)

    schemas = []
    for schema in inspector.get_schema_names():
        schemas.append(models.SchemaCreate(
            name=schema,
            comment=f"Schema {schema} automatically created",
        ))
    
    return schemas

def get_tables(schema: models.Schema):
    engine = next(get_data())
    inspector = inspect(engine)

    tables = []
    for table_name in inspector.get_table_names(schema=schema.name):
        tables.append(models.TableCreate(
            name=table_name,
            table_schema_id=schema.id,
            comment="Automatically created",
        ))
    
    return tables

def get_columns(schema: models.Schema, table: models.Table):
    engine = next(get_data())
    inspector = inspect(engine)

    columns = []
    for column in inspector.get_columns(table.name, schema=schema.name):
        columns.append(models.ColumnCreate(
            name=column['name'],
            table_id=table.id,
            type=str(column['type']),
            nullable=column['nullable'],
            default=column['default'],
            comment="automatically created",
        ))
    
    return columns

async def main():
    async with get_db_ctx() as session:
        schemas_repository = SchemasRepository(session)
        tables_repository = TableRepository(session)
        column_repository = TableColumnRepository(session)
        service = DbCoreService(schemas_repository, tables_repository, column_repository)
        
        pending_schemas = get_schemas()
        updated_schemas = await service.update_schemas(pending_schemas)
        print(f"Updated {len(updated_schemas)} schemas")

        for schema in updated_schemas:
            pending_tables = get_tables(schema)
            updated_tables = await service.update_tables(pending_tables)
            print(f"Schema {schema.name} updated with {len(updated_tables)} tables")

            for table in updated_tables:
                pending_columns = get_columns(schema, table)
                updated_columns = await service.update_columns(pending_columns)
                print(f"Table {table.name} updated with {len(updated_columns)} columns")

asyncio.run(main())
