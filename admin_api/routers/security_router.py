from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
import jwt

from .. import schemas
from ..repository import AuthRepository, Repository, get_auth_repository


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
    repository: AuthRepository = Depends(get_auth_repository),
) -> schemas.User:
    found = repository.get_user(email=input.email)
    
    if found:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    user_id = repository.create_user(
        name=input.name,
        email=input.email,
        password=pwd_context.hash(input.password),
    )

    repository.get_user(id=user_id)

    return 
