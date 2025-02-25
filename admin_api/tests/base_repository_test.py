import mock
from admin_api.repositories.base_repository import BaseRepository


class DatabaseMock:
    def cursor(self):
        return self

    def execute(self, query, params):
        return self

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def fetchall(self):
        return []

def test_execute_method():
    connection = DatabaseMock()
    connection.cursor = mock.Mock(return_value=connection)
    connection.execute = mock.Mock(return_value=connection)
    connection.fetchall = mock.Mock(return_value=connection)
    
    repository = BaseRepository(connection, "table")

    query = "SELECT * FROM table WHERE id = %(id)s"
    params = {"id": 1}
    
    repository._execute(query, params)
    connection.cursor.assert_called_once()
    connection.execute.assert_called_once_with(query, params)
    connection.fetchall.assert_called_once()
