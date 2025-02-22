from psycopg2.extensions import connection

class BaseRepository:
    def __init__(self, database: connection):
        self.database = database
    
    def _execute(self, query: str, params: dict):
        print(query)
        print(params)
        
        with self.database.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
