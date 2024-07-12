from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas import CreateUser, GetUser, UpdateUserPartial
import app.users.crud as user_crud
from app.db.database import get_async_session
from app.auth import get_user_from_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/search", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_user_from_token)])
async def is_user_exist(
        user: GetUser,
        session: AsyncSession = Depends(get_async_session)
):
    data = await user_crud.get(user, session)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect email or password")


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_user_from_token)])
async def create_user(
        new_user: CreateUser,
        session: AsyncSession = Depends(get_async_session)
):
    result = await user_crud.create(new_user, session)
    if result is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User is already exist")
    return {"status": "success"}


@router.patch("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_user_from_token)])
async def update_user_partial(
        user: GetUser,
        update_data: UpdateUserPartial,
        session: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.get(user, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect email or password")

    await user_crud.update_partial(user, update_data, session)
    return {"status": "success"}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_user_from_token)])
async def delete_user(
        user: GetUser,
        session: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.get(user, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect email or password")

    await user_crud.delete(user.id, session)
