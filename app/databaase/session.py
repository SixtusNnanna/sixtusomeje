from app.config import db_settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.databaase.base import Base

engine = create_async_engine(
    url=db_settings.POSTGRES_URL,
    echo=True,
)

ASYNC_SESSIONLOCAL = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session():
    async with ASYNC_SESSIONLOCAL() as session:
        yield session


async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
