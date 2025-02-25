from typing import Annotated
from fastapi.security import SecurityScopes
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from psycopg2.extensions import connection
from passlib.context import CryptContext

from admin_api import schemas
from admin_api.configuration import Configuration
from admin_api.repositories.users_repository import UsersRepository
from admin_api.services.base_service import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"])
    
    def __init__(self, database: connection):
        self.repository = UsersRepository(database)
    
    def decode_token(self, token: str):
        try:
            payload = jwt.decode(
                jwt=token,
                key=Configuration.secret_key,
                algorithms=[Configuration.algorithm]
            )
            username = payload.get("sub")
            return payload if username else None
        except jwt.PyJWTError:
            return None
    
    def register(self, data: schemas.UserCreate) -> schemas.User:
        found = self.repository.get_user(email=data.email)
    
        if found:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )
        
        data.password = self.pwd_context.hash(data.password)
        user_id = self.repository.create_user(data)

        return self.repository.get_user(id=user_id)

    def login(self, data: schemas.Login):
        user = self.repository.get_user(email=data.email)
    
        if not user or not self.pwd_context.verify(data.password, user.password):
            raise HTTPException(status_code=400, detail="incorrect username or password")
        
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

        return schemas.LoginOutput(access_token=encoded_jwt)
