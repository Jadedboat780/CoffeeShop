from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.db.models import UserOrm
from app.file import is_file_exist
from .shemas import CreateUser, GetUser
from ..auth.jwt import get_user_from_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/search", status_code=status.HTTP_204_NO_CONTENT)
@cache(60*30)
async def is_user_exist(
        user: GetUser,
        _authenticated=Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    '''Проверка существования пользователя'''
    get_user = await session.execute(select(UserOrm).where(user.email == UserOrm.email))
    data = get_user.scalars().one_or_none()
    if data is None or data.password != user.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect email or password")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        new_user: CreateUser,
        _authenticated=Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    '''Создание пользователя'''
    if new_user.image_url:
        is_exist = await is_file_exist(new_user.image_url)
        if is_exist is False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You didn't add a photo")

    query = UserOrm(**new_user.model_dump())
    session.add(query)
    await session.commit()
    return {"status": "success"}

# Код ниже задукомментирован, т.к. структура пользователя изменилась и необходимо переписать реализацию этих функций
# @router.patch("/{email}", status_code=status.HTTP_201_CREATED)
# async def update_user_partial(
#         email: EmailStr,
#         update_user: UpdateUserPartial,
#         session: AsyncSession = Depends(get_async_session)
# ):
#     user = await session.execute(select(UserOrm).where(email == UserOrm.email))
#     user = user.one_or_none()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found!")
#
#     if update_user.name:
#         user.name = update_user.name
#
#     if update_user.surname:
#         user.surname = update_user.surname
#
#     if update_user.email:
#         user.email = update_user.email
#
#     if update_user.password:
#         user.password = update_user.password
#
#     await session.commit()
#     return {"status": "success"}
#
#
# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(
#         id: Annotated[int, Path(ge=1)],
#         session: AsyncSession = Depends(get_async_session)
# ):
#     user = await session.get(UserOrm, id)
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")
#
#     await session.delete(user)
#     await session.commit()
#     return {"status": "success"}
