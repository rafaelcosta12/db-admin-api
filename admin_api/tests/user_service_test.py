import pytest
import mock
from fastapi import HTTPException
from admin_api import schemas
from admin_api.services.user_service import UserService


def test_user_update_should_fail_if_user_not_found():
    users_service = UserService(None)
    users_service.repository.get_user = mock.Mock(return_value=None)

    with pytest.raises(HTTPException, match=r".*not found.*"):
        users_service.update_user(1, schemas.UserUpdate(
            name="John Doe",
            email="teste@email.com",
            password="123456",
        ))