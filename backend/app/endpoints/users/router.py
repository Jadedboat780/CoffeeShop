from fastapi import APIRouter, Depends, status, HTTPException
import uuid
from .schemas import GetUser, UserData, CreateUser, UpdateUserPartial
from .crud import UserDAO

# dependencies=[Depends(get_user_from_token)])
router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/search/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_email(
        user_id: uuid.UUID,
        user_dao: UserDAO = Depends()
) -> UserData:
    user = await user_dao.get_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

    return UserData(**user.__dict__)


@router.post("/search", status_code=status.HTTP_200_OK)
async def get_user_by_email(
        user_data: GetUser,
        user_dao: UserDAO = Depends()
) -> UserData:
    user = await user_dao.get_by_email(email=user_data.email, password=user_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect email or password")

    return UserData(**user.__dict__)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: CreateUser,
        user_dao: UserDAO = Depends()
) -> UserData:
    user = await user_dao.create(new_user=user_data)
    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User is already exist")

    return UserData(**user.__dict__)


@router.patch("/{user_id}", status_code=status.HTTP_201_CREATED)
async def update_user_partial(
        user_id: uuid.UUID,
        update_data: UpdateUserPartial,
        user_dao: UserDAO = Depends()
) -> UserData:
    user = await user_dao.get_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

    updated_data = await user_dao.update_partial(user=user, update_data=update_data)
    return UserData(**updated_data.__dict__)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: uuid.UUID,
        user_dao: UserDAO = Depends()
):
    user = await user_dao.get_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

    await user_dao.delete(user=user)
