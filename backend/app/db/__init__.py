from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated

from .database import get_session
from .models import User, Coffee

SessionDep = Annotated[AsyncSession, Depends(get_session)]

__all__ = (User, Coffee, SessionDep)
