import os

from fastapi.security import OAuth2PasswordBearer

class Configuration:
    secret_key = os.environ.get("SECRET_KEY", "6f87f471ac3beba896e0895073f806466f87f471ac3beba896e0895073f80646")
    algorithm = os.environ.get("ALGORITHM", "HS256")
    token_expiration_minutes = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "3600"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
