import asyncio

from src.modules.auth.models import UserCreate
from src.modules.auth.repositories.user_repository import UsersRepository
from src.modules.auth.services.auth_service import AuthService
from src.db.session import get_db_ctx

async def create_admin_user():
    async with get_db_ctx() as session:
        repo = UsersRepository(session)
        auth = AuthService(repo)

        await auth.new_user(UserCreate(
            email="admin",
            is_active=True,
            is_admin=True,
            password="admin",
            name="admin",
        ))

asyncio.run(create_admin_user())
