import asyncio
from sqlalchemy import create_engine, MetaData, inspect

from src.modules.db_core import models
from src.modules.db_core.repositories import SchemasRepository, TableRepository, TableColumnRepository
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
            comment=f"Table {table_name} automatically created",
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
    schemas = get_schemas()
    async with get_db_ctx() as session:
        schemas_repository = SchemasRepository(session)
        tables_repository = TableRepository(session)
        column_repository = TableColumnRepository(session)

        for schema in schemas:
            db_schema = await schemas_repository.create(schema)
            tables = get_tables(db_schema)

            for table in tables:
                db_table = await tables_repository.create(table)
                print(f"Table {table.name} created in schema {db_schema.name}")

                for column in get_columns(db_schema, db_table):
                    await column_repository.create(column)
                    print(f"Column {column.name} created in table {table.name}")

asyncio.run(main())
