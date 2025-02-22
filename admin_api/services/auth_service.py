import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from psycopg2.extensions import connection
from passlib.context import CryptContext

from admin_api import schemas
from admin_api.configuration import Configuration
from admin_api.repository import AuthRepository
from admin_api.services.base_service import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"])
    
    def __init__(self, database: connection):
        self.repository = AuthRepository(database)
    
    def register(self, data: schemas.UserCreate) -> schemas.User:
        found = self.repository.get_user(email=data.email)
    
        if found:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )
        
        user_id = self.repository.create_user(
            name=data.name,
            email=data.email,
            password=self.pwd_context.hash(data.password))

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
