from typing import Annotated

from fastapi import Depends, HTTPException, status
import jwt

from .configuration import oauth2_scheme, Configuration
from ..modules.auth.repositories.user_repository import UsersRepository
from sqlalchemy.ext.asyncio import AsyncConnection
from ..db.session import get_db

def decode_token(token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=Configuration.secret_key,
            algorithms=[Configuration.algorithm]
        )
        username = payload.get("sub")
        return payload if username else None
    except jwt.PyJWTError:
        return None

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
    return user
