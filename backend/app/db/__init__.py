from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from .database import get_session
from .models import CoffeeOrm, UserOrm

SessionDep = Annotated[AsyncSession, Depends(get_session)]

__all__ = (UserOrm, CoffeeOrm, SessionDep)
