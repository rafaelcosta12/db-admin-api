from typing import Annotated
from fastapi import Depends
from psycopg2.extensions import connection

from admin_api.database import get_db_connection

class BaseService:
    @classmethod
    def from_di(cls, database: Annotated[connection, Depends(get_db_connection)]):
        return cls(database)
    
    def __init__(self, database: connection):
        self.database = database