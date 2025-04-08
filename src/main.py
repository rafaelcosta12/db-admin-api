from fastapi import FastAPI
from .modules.auth.routers import router as auth_router

app = FastAPI()
app.include_router(auth_router)
