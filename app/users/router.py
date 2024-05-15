from fastapi import APIRouter, Path, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from typing import Annotated

from app.db.database import get_async_session
from app.db.models import UserOrm
from .shemas import CreateUser, GetUser, UpdateUser, UpdateUserPartial

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{id}", response_model=GetUser)
async def get_user_by_id(
        id: Annotated[int, Path(ge=1)],
        session: AsyncSession = Depends(get_async_session)
):
    user = await session.get(UserOrm, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    return user


@router.get("/{email}", response_model=GetUser)
async def get_user_by_email(
        email: EmailStr,
        session: AsyncSession = Depends(get_async_session)
):
    user = await session.get(UserOrm, email) # выдаёт ошибку
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        new_user: CreateUser,
        session: AsyncSession = Depends(get_async_session)
):
    query = UserOrm(**new_user.model_dump())
    session.add(query)
    await session.commit()
    return {"status": "success"}


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_user(
        id: Annotated[int, Path(ge=1)],
        update_user: UpdateUser,
        session: AsyncSession = Depends(get_async_session)
):
    user = await session.get(UserOrm, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    user.name = update_user.name
    user.surname = update_user.surname
    user.email = update_user.email
    user.password = update_user.password

    await session.commit()
    return {"status": "success"}



@router.patch("/{id}", status_code=status.HTTP_201_CREATED)
async def update_user_partial(
        id: Annotated[int, Path(ge=1)],
        update_user: UpdateUserPartial,
        session: AsyncSession = Depends(get_async_session)
):
    user = await session.get(UserOrm, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    if update_user.name:
        user.name = update_user.name

    if update_user.surname:
        user.surname = update_user.surname

    if update_user.email:
        user.email = update_user.email

    if update_user.password:
        user.password = update_user.password

    await session.commit()
    return {"status": "success"}




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        id: Annotated[int, Path(ge=1)],
        session: AsyncSession = Depends(get_async_session)
):
    user = await session.get(UserOrm, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} not found!")

    await session.delete(user)
    await session.commit()
    return {"status": "success"}
