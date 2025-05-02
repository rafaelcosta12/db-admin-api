from pydantic import BaseModel, Field
from typing import Optional, Literal, TypeVar, Generic
import datetime

T = TypeVar('T')

class UserBase(BaseModel):
    name: str
    email: str
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    profile_img: Optional[str] = None

class UserUpdate(UserBase):
    pass

class UserCreate(UserBase):
    password: Optional[str] = None
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = False

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

class PaginationSearchResult(BaseModel, Generic[T]):
    total: int
    page: int
    items: list[T]

class BasePaginationSearchFilter(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order: Literal["asc", "desc"] = "desc"

class UserSearchFilter(BasePaginationSearchFilter):
    order_by: Literal["created_at", "updated_at"] = "created_at"
    name: Optional[str] = None
    email: Optional[str] = None
    text: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None

class UserGroupBase(BaseModel):
    name: str

class UserGroupCreate(UserGroupBase):
    pass

class UserGroupUpdate(UserGroupBase):
    pass

class UserGroup(UserGroupBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class UserGroupWithDetails(UserGroup):
    user_count: int = 0

class UserGroupSearchFilter(BasePaginationSearchFilter):
    order_by: Literal["created_at", "updated_at"] = "created_at"
    name: Optional[str] = None
    text: Optional[str] = None

class UserGroupMember(BaseModel):
    user_id: int
    group_id: int

class UserCountByGroup(BaseModel):
    user_count: int
    group_id: int
