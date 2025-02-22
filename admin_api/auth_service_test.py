import pytest
from fastapi import HTTPException

from admin_api.services.auth_service import AuthService
from admin_api.schemas import User, UserCreate
from admin_api import schemas
import mock


def test_register_should_fail_if_exists_email():
    auth_service = AuthService(None)
    auth_service.repository.create_user = mock.Mock(return_value=1)
    auth_service.repository.get_user = mock.Mock(return_value={
        "id": 1,
        "name": "Test User",
        "email": "teste@email.com",
        "password": "hashed_password",
        "created_at": "2021-09-01T00:00:00",
        "updated_at": "2021-09-01T00:00:00",
        "disabled": False
    })

    with pytest.raises(HTTPException, match=r".*already registered.*"):
        auth_service.register(UserCreate(name="Test User", email="teste@email.com", password="hashed_password"))

def test_register_should_pass_if_ok():
    auth_service = AuthService(None)
    auth_service.repository.create_user = mock.Mock(return_value=1)
    auth_service.repository.get_user = mock.Mock(side_effect=[None, User(**{
        "id": 1,
        "name": "Test User",
        "email": "teste@email.com",
        "password": "hashed_password",
        "created_at": "2021-09-01T00:00:00",
        "updated_at": "2021-09-01T00:00:00",
        "disabled": False
    })])

    result = auth_service.register(UserCreate(name="Test User", email="teste@email.com", password="hashed_password"))
    assert result.id == 1
    assert result.name == "Test User"

def test_login_should_fail_if_no_user_found():
    auth_service = AuthService(None)
    auth_service.repository.get_user = mock.Mock(return_value=None)

    with pytest.raises(HTTPException, match=r".*incorrect.*"):
        auth_service.login(schemas.Login(email="exemplo@email.com", password="hashed_password"))

def test_login_should_fail_if_wrong_password():
    auth_service = AuthService(None)
    auth_service.repository.get_user = mock.Mock(return_value=User(
        id=1,
        name="Test User", 
        email="teste@email.com", 
        password="$2b$12$Z7Hcnh6.d6tcO3IHmjUJg.B/rwBlILzHlFrUqhlLP/A8bzXdelBXi", # passwd
        created_at="2021-09-01T00:00:00", 
        updated_at="2021-09-01T00:00:00", 
        disabled=False))

    with pytest.raises(HTTPException, match=r".*incorrect.*"):
        auth_service.login(schemas.Login(email="exemplo@email.com", password="wrong_password"))

def test_login_should_success_if_ok():
    auth_service = AuthService(None)
    auth_service.repository.get_user = mock.Mock(return_value=User(
        id=1,
        name="Test User", 
        email="teste@email.com", 
        password="$2b$12$Z7Hcnh6.d6tcO3IHmjUJg.B/rwBlILzHlFrUqhlLP/A8bzXdelBXi", # passwd
        created_at="2021-09-01T00:00:00", 
        updated_at="2021-09-01T00:00:00", 
        disabled=False))

    auth_service.login(schemas.Login(email="exemplo@email.com", password="passwd"))
