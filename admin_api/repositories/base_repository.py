from psycopg2.extensions import connection
from pydantic import BaseModel

class BaseRepository:
    def __init__(self, database: connection, table_name: str, pk_name: str = 'id'):
        self.database = database
        self.table_name = table_name
        self.pk_name = pk_name
    
    def _execute(self, query: str, params: dict):
        print(query)
        print(params)
        
        with self.database.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def _get_columns_from_schema(self, schema):
        return list(schema.model_fields.keys())

    def _select(self, columns: list, where = []):
        sql = """
        SELECT {projection}
        FROM {table_name}
        """.format(
            projection=', '.join(columns),
            table_name=self.table_name,
        )
        
        if where:
            sql += 'WHERE ' + " AND ".join(where)
        
        return sql

    def _execute_select(self, schema, values, where = []) -> list:
        columns = self._get_columns_from_schema(schema)
        rows = []
        for row in self._execute(self._select(columns, where), values):
            rows.append(schema(**{key: val for key, val in zip(columns, row)}))
        return rows
    
    def _insert(self, data: BaseModel) -> int:
        data = data.model_dump()
        columns = list(data.keys())
        query = f"""
        INSERT INTO {self.table_name} ({', '.join(columns)}) 
        VALUES ({', '.join([f'%({name})s' for name in columns])})
        RETURNING {self.pk_name};
        """
        rows = self._execute(query, data)
        return rows[0][0]

    def _update(self, pk, data: BaseModel):
        data = data.model_dump(exclude={self.pk_name})
        query = f"""
        UPDATE admin_api.users
        SET {", ".join([f"{key} = %({key})s" for key in data.keys()])}
        WHERE id = %({self.pk_name})s
        RETURNING {self.pk_name};
        """
        self._execute(query, {**data, self.pk_name: pk})