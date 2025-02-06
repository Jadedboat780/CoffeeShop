from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import Annotated

from .database import get_session
from .models import UserOrm, CoffeeOrm

SessionDep = Annotated[AsyncSession, Depends(get_session)]

__all__ = (UserOrm, CoffeeOrm, SessionDep)
