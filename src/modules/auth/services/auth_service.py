import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from passlib.context import CryptContext
import uuid

from .. import models
from ....core.configuration import Configuration
from ..repositories.user_repository import UsersRepository

class AuthService:
    def __init__(self, repository: UsersRepository):
        self.pwd_context = CryptContext(schemes=["bcrypt"])
        self.repository = repository
    
    async def list_users(self, filter: models.UserSearchFilter) -> models.PaginationSearchResult[models.User]:
        return await self.repository.list_paged(filter)
    
    async def find_user(self, user_id: int) -> models.User:
        user = await self.repository.find(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def new_user(self, data: models.UserCreate) -> models.User:
        await self._check_user_already_exists(data)
        data.password = self.pwd_context.hash(str(uuid.uuid4()))
        user_id = await self.repository.insert(data)
        user = await self.repository.find(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def _check_user_already_exists(self, data):
        found = await self.repository.find(email=data.email)
        if found:
            raise HTTPException(status_code=400, detail="Username already registered")

    async def login(self, data: models.Login):
        user = await self.repository.find(email=data.email)

        if not user or not self.pwd_context.verify(data.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        expire = datetime.now(timezone.utc) + timedelta(minutes=Configuration.token_expiration_minutes)
        
        encoded_jwt = jwt.encode(
            payload={
                "sub": user.email,
                "scopes": [],
                "exp": expire,
            }, 
            key=Configuration.secret_key,
            algorithm=Configuration.algorithm,
        )

        return models.LoginOutput(access_token=encoded_jwt, user=user)

    async def update_user(self, user_id: int, data: models.UserUpdate) -> models.User:
        user = await self.repository.find(id=user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return await self.repository.update(user_id, data)
    
    async def update_user_profile_img(self, user_id: int, img_url: str) -> models.User:
        user = await self.repository.find(id=user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.profile_img = img_url
        return await self.repository.update(user_id, models.UserUpdate(**user.dict()))

    async def delete_user(self, user_id: int) -> None:
        user = await self.repository.find(id=user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.repository.delete(user_id)
