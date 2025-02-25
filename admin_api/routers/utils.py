from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import SecurityScopes
from pytest import Session

from admin_api.configuration import oauth2_scheme
from admin_api.services.auth_service import AuthService


def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: AuthService = Depends(AuthService.from_di),
):
    claims = auth_service.decode_token(token)
    
    if not claims:
        raise HTTPException(status_code=401, detail="invalid token")
    
    email = claims.get("sub")
    user = auth_service.repository.get_user(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="user not found, invalid token")
    
    scopes = claims.get("scopes", [])
    for scope in security_scopes.scopes:
        if scope not in scopes:
            raise HTTPException(status_code=401, detail="not enough permissions")

    return user
