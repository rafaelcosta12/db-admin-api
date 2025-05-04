from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker
)

dsn_default = "postgresql+asyncpg://postgres:postgres@localhost:5432/devstacker"

# 1. Configuração da Engine Assíncrona
def create_db_engine(dsn: str) -> AsyncEngine:
    return create_async_engine(dsn, echo=True,)

# 2. Factory de Sessões Assíncronas
def create_async_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,  # Importante para evitar comportamentos inesperados
    )

# 3. Instâncias Globais (únicas por aplicação)
_sessions = {
    "main": create_async_session_factory(create_db_engine(dsn_default)),
    "dummy": create_async_session_factory(create_db_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/dummy_application")),
}

# 4. Dependência para injeção em rotas FastAPI
async def get_db(name: Optional[str] = None) -> AsyncGenerator[AsyncSession]:
    async with _sessions[name or "main"]() as session:
        try:
            yield session
            await session.commit()  # Commit automático se não houver erros
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()  # Garante o fechamento

# 5. Context Manager Assíncrono (opcional)
@asynccontextmanager
async def get_db_ctx(name: Optional[str] = None) -> AsyncGenerator[AsyncSession]:
    async with _sessions[name or "main"]() as session:
        try:
            yield session
            await session.commit()  # Commit automático se não houver erros
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()  # Garante o fechamento
