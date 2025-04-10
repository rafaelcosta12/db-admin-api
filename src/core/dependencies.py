from typing import Annotated
import logging

from fastapi import Depends, HTTPException, status
import jwt

from .configuration import oauth2_scheme, Configuration
from ..modules.auth.repositories.user_repository import UsersRepository
from sqlalchemy.ext.asyncio import AsyncConnection
from ..db.session import get_db
from ..modules.auth.models import User

def decode_token(token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=Configuration.secret_key,
            algorithms=[Configuration.algorithm]
        )
        username = payload.get("sub")
        return payload if username else None
    except jwt.PyJWTError as err:
        logging.error("Token decode error", exc_info=err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    conn: Annotated[AsyncConnection, Depends(get_db)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = {"email": email}
    
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    user = await UsersRepository(conn).find(email=token_data["email"])
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise credentials_exception
    
    return user

async def should_be_logged_in(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to be logged in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

async def should_be_admin(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough permissions"
        )
    return current_user
