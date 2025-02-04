from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from .database import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

__all__ = (SessionDep,)
