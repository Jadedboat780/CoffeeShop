from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import config

engine = create_async_engine(url=config.DATABASE_URL, pool_size=10, max_overflow=15)
session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):
    """Base model"""

    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a session to db"""
    async with session_maker() as session:
        yield session
