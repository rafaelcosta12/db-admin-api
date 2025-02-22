from fastapi import APIRouter, Depends

from .. import schemas
from ..services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(
    data: schemas.Login,
    service: AuthService = Depends(AuthService.from_di)
) -> schemas.LoginOutput:
    return service.login(data)

@router.post("/register")
async def register(
    input: schemas.UserCreate,
    service: AuthService = Depends(AuthService.from_di),
) -> schemas.User:
    return service.register(input)
