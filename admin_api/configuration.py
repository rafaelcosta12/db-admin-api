import os

from fastapi.security import OAuth2PasswordBearer

class Configuration:
    secret_key = os.environ.get("SECRET_KEY")
    algorithm = os.environ.get("ALGORITHM", "HS256")
    token_expiration_minutes = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60)

oauth2_scheme = OAuth2PasswordBearer()
