from admin_api.repositories.base_repository import BaseRepository
from admin_api import schemas


class UsersRepository(BaseRepository):
    def __init__(self, database):
        super().__init__(database, table_name="admin_api.users")

    def get_user(self, id: int = None, email: str = None):
        where = []
        
        if id:
            where.append("id = %(id)s")

        if email:
            where.append("email = %(email)s")

        for row in self._execute_select(schemas.User, {"id": id, "email": email}, where):
            return row

    def create_user(self, data: schemas.UserCreate) -> int:
        return self._insert(data)

    def update_user(self, data: schemas.UserUpdate):
        _data = _data.model_dump(exclude={"id"})
        query = f"""
        UPDATE admin_api.users
        SET {", ".join([f"{key} = %({key})s" for key in _data.keys()])}
        WHERE id = %s;
        """
        self._execute(query, {**_data, "id": data.id})
