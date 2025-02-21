from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import tables_router, security_router

app = FastAPI()

app.include_router(tables_router.router)
app.include_router(security_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)
