from typing import Annotated
from fastapi import APIRouter, Depends, Security

from .. import schemas
from ..services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("")
async def list_users(
    service: UserService = Depends(UserService.from_di),
) -> list[schemas.User]:
    return service.repository.list_users()

@router.get("/me")
def me(
    user: Annotated[schemas.User, Security(UserService.get_current_user)],
) -> schemas.User:
    return user

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    input_data: schemas.UserUpdate,
    service: UserService = Depends(UserService.from_di),
) -> schemas.User:
    return service.update_user(user_id, input_data)

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    service: UserService = Depends(UserService.from_di),
) -> schemas.User:
    return service.repository.get_user(user_id)
