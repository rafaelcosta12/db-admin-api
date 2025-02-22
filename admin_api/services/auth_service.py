from fastapi import HTTPException
from admin_api.repository import AuthRepository
from psycopg2.extensions import connection
from passlib.context import CryptContext

from admin_api import schemas


class AuthService:
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
        
        # access_token = create_access_token(found, scopes=form_data.scopes)

        return schemas.LoginOutput(access_token="")

    def logout(self):
        pass