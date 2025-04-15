from fastapi import APIRouter, Depends, File, Query
from typing import Annotated

from . import models
from .services.auth_service import AuthService
from .repositories.user_repository import UsersRepository
from ...db.session import get_db
from ...core.dependencies import get_current_user, should_be_logged_in, should_be_admin
import httpx

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
users_router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(should_be_logged_in)])

def get_auth_service(conn=Depends(get_db)):
    repo = UsersRepository(conn)
    return AuthService(repo)

@auth_router.post("/login")
async def login(
    data: models.Login,
    service: AuthService = Depends(get_auth_service)
) -> models.LoginOutput:
    return await service.login(data)

@users_router.get("/me")
async def current_user(
    user: models.User = Depends(get_current_user),
) -> models.User:
    return user

@users_router.get("")
async def list_users(
    filter: Annotated[models.UserSearchFilter, Query()],
    service: AuthService = Depends(get_auth_service),
) -> models.PaginationSearchResult[models.User]:
    return await service.list_users(filter)

@users_router.get("/{user_id}")
async def find_users(
    user_id: int,
    service: AuthService = Depends(get_auth_service),
) -> models.User:
    return await service.find_user(user_id)

@users_router.post("", dependencies=[Depends(should_be_admin)])
async def new_user(
    input: models.UserCreate,
    service: AuthService = Depends(get_auth_service),
) -> models.User:
    return await service.new_user(input)

@users_router.put("/{user_id}", dependencies=[Depends(should_be_admin)])
async def update_user(
    user_id: int,
    input: models.UserUpdate,
    service: AuthService = Depends(get_auth_service),
) -> models.User:
    return await service.update_user(user_id, input)

@users_router.delete("/{user_id}", dependencies=[Depends(should_be_admin)], status_code=204)
async def delete_user(
    user_id: int,
    service: AuthService = Depends(get_auth_service),
):
    await service.delete_user(user_id)

@users_router.post("/{user_id}/image", dependencies=[Depends(should_be_admin)])
async def update_image(
    user_id: int,
    file: Annotated[bytes, File()],
    service: AuthService = Depends(get_auth_service),
):
    # TODO: save file to aws s3 and return the url
    async with httpx.AsyncClient() as client:
        r = await client.get("https://picsum.photos/200")
        assert r.status_code == 302
        image_url = r.headers["location"]
    return await service.update_user_profile_img(user_id, image_url)
