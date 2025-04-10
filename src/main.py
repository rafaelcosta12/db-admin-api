from fastapi import FastAPI
from .modules.auth.routers import auth_router, users_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path="/api")
app.include_router(auth_router)
app.include_router(users_router)

app.add_middleware(
     CORSMiddleware,
     allow_origins=["http://localhost:5173"],
     allow_credentials=True,
     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
     allow_headers=["*"],
 )