from fastapi.testclient import TestClient
import pytest
from admin_api.repositories.users_repository import UsersRepository
from admin_api.services.auth_service import AuthService
from admin_api import app, database, schemas
import random

client = TestClient(app)
default_user = schemas.UserCreate(
    name="Test User",
    email="blueman@email.com",
    password="passwd@123")

def get_random_str(k=10):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=k))

def ensure_test_user_exists():
    connection = next(database.get_db_connection())
    service = AuthService(connection)
    user = service.repository.get_user(email=default_user.email)
    if user is None:
        service.register(default_user)
        connection.commit()

@pytest.fixture(scope="module", autouse=True)
def setup():
    ensure_test_user_exists()

def test_register_user_ok():
    input_data = {
        "name": "Test User",
        "email": f"{get_random_str()}@email.com",
        "password": "hashed_password",
        "disabled": False
    }
    response = client.post("/auth/register", json=input_data)
    assert response.status_code == 200, response.text
    
    output_data = response.json()
    assert output_data["name"] == input_data["name"]
    assert output_data["email"] == input_data["email"]
    assert output_data["disabled"] == input_data["disabled"]
    assert "id" in output_data
    assert "created_at" in output_data
    assert "updated_at" in output_data

def test_login_ok():
    input_data = {
        "email": default_user.email,
        "password": default_user.password,
    }
    response = client.post("/auth/login", json=input_data)
    assert response.status_code == 200, response.text

def test_user_update_ok():
    pass