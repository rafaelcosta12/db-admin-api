from pydantic import BaseModel
from typing import List, Optional, Any
import datetime

class ColumnDetails(BaseModel):
    name: str
    udt_name: str
    is_nullable: str
    character_maximum_length: Optional[int]
    default: Optional[str]


class ConstraintDetails(BaseModel):
    name: str
    type: str
    column_name: Optional[str]
    references: Optional[str]


class TableDetails(BaseModel):
    name: str
    type: str
    schema: str
    columns: Optional[List[ColumnDetails]] = None
    constraints: Optional[List[ConstraintDetails]] = None

    @property
    def pk(self):
        for constraint in self.constraints:
            if constraint.type == "PRIMARY KEY":
                return constraint.column_name
    
    @property
    def key(self):
        return f"{self.schema}.{self.name}"


class TableRows(BaseModel):
    data: List[dict[str, Any]]
    total: int


class TableRowOperation(BaseModel):
    pk: Any
    message: str
    data: Optional[dict[str, Any]]


class UserBase(BaseModel):
    name: str
    email: str
    disabled: Optional[bool] = None

class User(UserBase):
    id: int
    password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class UserUpdate(UserBase):
    pass

class UserCreate(UserBase):
    password: str

class Login(BaseModel):
    email: str
    password: str

class LoginOutput(BaseModel):
    access_token: str