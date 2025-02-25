from typing import Annotated
from fastapi.security import SecurityScopes
from admin_api.configuration import oauth2_scheme
from admin_api.repositories.users_repository import UsersRepository
from admin_api.services.auth_service import AuthService
from admin_api.services.base_service import BaseService
from psycopg2.extensions import connection
from admin_api import schemas
from fastapi import Depends, HTTPException


class UserService(BaseService):
    def __init__(self, database: connection):
        self.repository = UsersRepository(database)
    
    @classmethod    
    def get_current_user(
        cls,
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_service: AuthService = Depends(AuthService.from_di),
    ):
        claims = auth_service.decode_token(token)
        
        if not claims:
            raise HTTPException(status_code=401, detail="invalid token")
        
        email = claims.get("sub")
        user = auth_service.repository.get_user(email=email)
        if not user:
            raise HTTPException(status_code=404, detail="user not found, invalid token")
        
        scopes = claims.get("scopes", [])
        for scope in security_scopes.scopes:
            if scope not in scopes:
                raise HTTPException(status_code=401, detail="not enough permissions")

        return user
    
    def update_user(self, id: int, data: schemas.UserUpdate):
        user = self.repository.get_user(id=id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        self.repository.update_user(id, data)

        return self.repository.get_user(id=id)