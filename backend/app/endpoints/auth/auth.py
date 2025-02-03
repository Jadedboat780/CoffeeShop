from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from db.database import get_async_session
from db.models import UserOrm
from .schemas import TokenInfo
from .jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
        user: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_async_session),
) -> TokenInfo:
    '''Получение jwt токена'''
    get_user = await session.execute(select(UserOrm).where(user.username == UserOrm.email and user.password == UserOrm.password))
    get_user = get_user.scalars().one_or_none()
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    access_token = create_access_token({'id': str(get_user.id)})
    return TokenInfo(access_token=access_token, token_type="bearer")
