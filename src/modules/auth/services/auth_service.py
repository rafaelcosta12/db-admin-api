import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from passlib.context import CryptContext

from .. import models
from ....core.configuration import Configuration
from ..repositories.user_repository import UsersRepository

class AuthService:
    def __init__(self, repository: UsersRepository):
        self.pwd_context = CryptContext(schemes=["bcrypt"])
        self.repository = repository
    
    async def new_user(self, data: models.UserCreate) -> models.User:
        await self._check_user_already_exists(data)
        data.password = self.pwd_context.hash(data.password)
        user_id = self.repository.insert(data)
        return self.repository.find(id=user_id)

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

        return models.LoginOutput(access_token=encoded_jwt)
