from fastapi import APIRouter, Depends

from . import models
from .services.auth_service import AuthService
from .repositories.user_repository import UsersRepository
from ...db.session import get_db

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
async def register(
    input: models.UserCreate,
    service: AuthService = Depends(get_auth_service),
) -> models.User:
    return await service.register(input)
