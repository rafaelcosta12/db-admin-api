from pydantic import BaseModel
from typing import Optional

class ColumnBase(BaseModel):
    table_id: int
    name: str
    type: str
    nullable: bool
    default: Optional[str] = None
    autoincrement: bool = False
    comment: Optional[str] = None

class ColumnCreate(ColumnBase):
    pass

class ColumnUpdate(ColumnBase):
    pass

class Column(ColumnBase):
    id: int

class TableBase(BaseModel):
    name: str
    comment: Optional[str] = None
    table_schema_id: int

class TableCreate(TableBase):
    pass

class TableUpdate(TableBase):
    pass

class Table(TableBase):
    id: int
    columns: list[Column] = []
    primary_keys: list[str] = []
    # foreign_keys: list['ForeignKey'] = []
    # indexes: list['Index'] = []

class SchemaBase(BaseModel):
    name: str
    comment: Optional[str] = None

class SchemaCreate(SchemaBase):
    pass

class SchemaUpdate(SchemaBase):
    pass

class Schema(SchemaBase):
    id: int
    tables: list[Table] = []

class SchemaNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.code = 404