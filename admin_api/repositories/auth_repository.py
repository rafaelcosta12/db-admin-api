
from admin_api.repositories.base_repository import BaseRepository
from admin_api import schemas


class AuthRepository(BaseRepository):
    def get_user(self, id: int = None, email: str = None):
        columns = schemas.User.model_fields.keys()
        query = f"""
        SELECT {', '.join(columns)}
        FROM admin_api.users
        """
        where = []
        
        if id:
            where.append("id = %(id)s")

        if email:
            where.append("email = %(email)s")

        if where:
            query += 'WHERE ' + " AND ".join(where)
        
        for row in self._execute(query, {"id": id, "email": email}):
            return schemas.User(**{key: val for key, val in zip(columns, row)})

    def create_user(self, name, email, password) -> int:
        query = """
        INSERT INTO admin_api.users (name, email, password) 
        VALUES (%s, %s, %s) 
        RETURNING id;
        """
        rows = self._execute(query, [name, email, password])
        return rows[0][0]
