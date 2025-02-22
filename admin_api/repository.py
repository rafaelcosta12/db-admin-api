from typing import Annotated, List, Any
from fastapi import Depends
from psycopg2.extensions import connection

from .database import get_db_connection
from .repositories.base_repository import BaseRepository
from . import schemas


class Repository:
    def __init__(self, database: connection):
        self.database = database

    def map_values(self, values: list, columns: List[schemas.ColumnDetails]):
        result = {}
        for column, value in zip(columns, values):
            result[column.name] = value
        return result

    def get_table_details(self, cur=None):
        cur = cur or self.database.cursor()

        table_query = """
        SELECT table_name, table_type, table_schema
        FROM information_schema.tables
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY table_schema, table_name;
        """
        cur.execute(table_query)
        rows = cur.fetchall()
        result: List[schemas.TableDetails] = []

        col_names = ["name", "type", "schema"]
        for table in rows:
            k = {key: val for key, val in zip(col_names, table)}
            result.append(schemas.TableDetails(**k))

        return result

    def get_table_details_from_table_name(self, schema, table):
        cur = self.database.cursor()

        table_query = """
        SELECT table_name, table_type, table_schema
        FROM information_schema.tables
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            AND table_schema = %s AND table_name = %s
        ORDER BY table_schema, table_name;
        """
        cur.execute(table_query, (schema, table))
        table_details = cur.fetchone()

        col_names = ["name", "type", "schema"]
        
        k = {key: val for key, val in zip(col_names, table_details)}
        table_details = schemas.TableDetails(**k)
        
        table_details.columns = self.get_table_columns(table_details.schema, table_details.name, cur=cur)
        table_details.constraints = self.get_table_constraints(table_details.schema, table_details.name, cur=cur)

        return table_details

    def get_table_columns(self, schema, table, cur=None):
        cur = cur or self.database.cursor()
        result = []

        # Query to get column details for the table
        column_query = """
        SELECT column_name, udt_name, is_nullable, column_default, character_maximum_length
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position;
        """
        cur.execute(column_query, (schema, table))
        rows = cur.fetchall()

        col_names = ["name", "udt_name", "is_nullable", "default", "character_maximum_length"]
        for row in rows:
            k = {key: val for key, val in zip(col_names, row)}
            result.append(schemas.ColumnDetails(**k))
        
        return result

    def get_table_constraints(self, schema, table, cur=None):
        cur = cur or self.database.cursor()
        result = []
        
        # Query to get constraints for the table
        constraint_query = """
        SELECT tc.constraint_name, tc.constraint_type, kcu.column_name, ccu.table_schema AS foreign_table_schema, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints tc
        LEFT JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
            AND tc.table_name = kcu.table_name
        LEFT JOIN information_schema.constraint_column_usage ccu
            ON tc.constraint_name = ccu.constraint_name
            AND tc.table_schema = ccu.table_schema
        WHERE tc.table_schema = %s AND tc.table_name = %s
        ORDER BY tc.constraint_name;
        """
        cur.execute(constraint_query, (schema, table))
        rows = cur.fetchall()

        col_names = ["name", "type", "column_name"]
        for row in rows:
            k = {key: val for key, val in zip(col_names, row)}
            k["references"] = ".".join(row[3:]) if k["type"] == 'FOREIGN KEY' else None
            result.append(schemas.ConstraintDetails(**k))
        
        return result

    def list_rows(self, schema: str, table: str):
        list_query = f"SELECT * FROM {schema}.{table};"
        
        with self.database.cursor() as cur:
            columns = self.get_table_columns(schema, table)
            cur.execute(list_query)
            return [self.map_values(row, columns) for row in cur.fetchall()]
    
    def count_rows(self, schema: str, table: str):
        count_query = f"SELECT COUNT(*) FROM {schema}.{table};"
        
        with self.database.cursor() as cur:
            cur.execute(count_query)
            return cur.fetchone()[0]

    def insert(self, schema: str, table: str, data: dict[str, Any]):
        insert_query = "INSERT INTO {schema}.{table} ({columns}) VALUES ({values}) RETURNING {pk};"

        table_details = self.get_table_details_from_table_name(schema, table)
        with self.database.cursor() as cur:
            cur.execute(insert_query.format(
                schema=schema, 
                table=table, 
                columns=",".join(data.keys()),
                values=",".join(["%s" for _ in range(len(data))]),
                pk=table_details.pk), list(data.values()))
            return cur.fetchone()[0]

    def get_row_by_pk(self, schema: str, table: str, row_pk: Any):
        select_query = "SELECT * FROM {schema}.{table} WHERE {pk} = %s;"

        table_details = self.get_table_details_from_table_name(schema, table)

        with self.database.cursor() as cur:
            cur.execute(select_query.format(schema=schema, table=table, pk=table_details.pk), [row_pk])
            return self.map_values(cur.fetchone(), table_details.columns)

    def update(self, schema: str, table: str, row_pk: Any, data: dict):
        update_query = "UPDATE {schema}.{table} SET {values} WHERE {pk} = %s;"
        table_details = self.get_table_details_from_table_name(schema, table)
        with self.database.cursor() as cur:
            cur.execute(update_query.format(
                schema=schema, 
                table=table, 
                values=", ".join([f"{column_name} = %s" for column_name in data.keys()]),
                pk=table_details.pk), 
                [*data.values(), row_pk])

    def delete(self, schema: str, table: str, row_pk: Any):
        delete_query = "DELETE FROM {schema}.{table} WHERE {pk} = %s;"
        table_details = self.get_table_details_from_table_name(schema, table)
        with self.database.cursor() as cur:
            cur.execute(delete_query.format(schema=schema, table=table, pk=table_details.pk), [row_pk])


def get_repository(database: Annotated[connection, Depends(get_db_connection)]):
    return Repository(database)


def get_auth_repository(database: Annotated[connection, Depends(get_db_connection)]):
    return Repository(database)