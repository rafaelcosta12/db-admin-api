from admin_api.repositories.users_repository import UsersRepository
from admin_api.services.base_service import BaseService
from psycopg2.extensions import connection
from admin_api import schemas
from fastapi import HTTPException


class UserService(BaseService):
    def __init__(self, database: connection):
        self.repository = UsersRepository(database)
    
    def update_user(self, id: int, data: schemas.UserUpdate):
        user = self.repository.get_user(id=id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        self.repository.update_user(data)