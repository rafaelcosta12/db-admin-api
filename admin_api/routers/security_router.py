from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
import jwt

from .. import schemas
from ..repository import Repository, get_auth_repository
from ..services.auth_service import AuthService


pwd_context = CryptContext(schemes=["bcrypt"])
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(
    input: schemas.Login,
    repository: Repository = Depends(get_auth_repository)
):
    return {"message": "Login successful"}

@router.post("/logout")
async def logout(
    repository: Repository = Depends(get_auth_repository)
):
    return {"message": "Logout successful"}

@router.post("/register")
async def register(
    input: schemas.UserCreate,
    service: AuthService = Depends(AuthService.from_di),
) -> schemas.User:
    return service.register(input)
