from fastapi import APIRouter, Depends

from . import models
from .services.auth_service import AuthService
from .repositories.user_repository import UsersRepository
from ...db.session import get_db
from ...core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_auth_service(conn=Depends(get_db)):
    repo = UsersRepository(conn)
    return AuthService(repo)

@router.post("/login")
async def login(
    data: models.Login,
    service: AuthService = Depends(get_auth_service)
) -> models.LoginOutput:
    return await service.login(data)

@router.post("/register")
async def register_new_user(
    input: models.UserCreate,
    service: AuthService = Depends(get_auth_service),
) -> models.User:
    return await service.new_user(input)

@router.get("/me", response_model=models.User)
async def current_user(
    user: models.User = Depends(get_current_user),
) -> models.User:
    return user
