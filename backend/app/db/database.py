from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from config import settings

engine = create_async_engine(url=settings.DATABASE_URL, pool_size=5, max_overflow=10)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    '''Получение сессии'''
    async with async_session_maker() as session:
        yield session
