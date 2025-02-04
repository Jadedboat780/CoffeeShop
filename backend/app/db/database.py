from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from app.config import config

engine = AsyncEngine(create_engine(url=config.DATABASE_URL, pool_size=10, max_overflow=15))
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a session to db"""
    async with session_maker() as session:
        yield session

