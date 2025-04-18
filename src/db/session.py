import os
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker
)

DSN = os.environ.get("DSN", "postgresql+asyncpg://postgres:postgres@localhost:5432/devstacker")

# 1. Configuração da Engine Assíncrona
def create_db_engine() -> AsyncEngine:
    """Cria a engine de conexão assíncrona com o banco"""
    return create_async_engine(
        DSN,  # Ex: "postgresql+asyncpg://user:pass@localhost/db"
        echo=True,  # Log de queries (True em desenvolvimento)
    )

# 2. Factory de Sessões Assíncronas
def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Cria a factory para gerar sessões de banco"""
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,  # Importante para evitar comportamentos inesperados
    )

# 3. Instâncias Globais (únicas por aplicação)
engine = create_db_engine()
SessionLocal = create_session_factory(engine)

# 4. Dependência para injeção em rotas FastAPI
async def get_db() -> AsyncGenerator[AsyncSession]:
    """Gerador de sessões para injeção de dependência"""
    async with SessionLocal() as session:
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
async def get_db_ctx() -> AsyncGenerator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()  # Commit automático se não houver erros
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()  # Garante o fechamento