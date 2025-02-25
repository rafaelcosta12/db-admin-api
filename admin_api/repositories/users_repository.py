from admin_api.repositories.base_repository import BaseRepository
from admin_api import schemas


class UsersRepository(BaseRepository):
    def __init__(self, database):
        super().__init__(database, table_name="admin_api.users")

    def list_users(self, id: int = None, email: str = None):
        where = []
        
        if id:
            where.append("id = %(id)s")

        if email:
            where.append("email = %(email)s")

        return self._execute_select(schemas.User, {"id": id, "email": email}, where)
    
    def get_user(self, id: int = None, email: str = None):
        for row in self.list_users(id, email):
            return row

    def create_user(self, data: schemas.UserCreate) -> int:
        return self._insert(data)

    def update_user(self, user_id: int, data: schemas.UserUpdate):
        return self._update(user_id, data)
