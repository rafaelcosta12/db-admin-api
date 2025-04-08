from pydantic import BaseModel
from typing import Optional
import datetime

class UserBase(BaseModel):
    name: str
    email: str
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None

class UserUpdate(UserBase):
    pass

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class UserPassword(User):
    password: str

class Login(BaseModel):
    email: str
    password: str

class LoginOutput(BaseModel):
    access_token: str
    user: User
