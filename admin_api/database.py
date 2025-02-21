import psycopg2
import os

DSN = os.environ.get("DSN", "postgresql://postgres:postgres@localhost:5432/devstacker")

def get_db_connection():
    with psycopg2.connect(DSN) as conn:
        yield conn
        conn.commit()

