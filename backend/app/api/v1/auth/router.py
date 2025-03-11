from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.api.v1.users.crud import UserDAO
from .schemas import TokenInfo
from .jwt import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_dao: UserDAO = Depends()
) -> TokenInfo:
    """ OAuth2 compatible token login, get an access token for future requests"""
    user = await user_dao.get_by_email(email=user_data.username, password=user_data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


# @router.post("/refresh/")
# async def refresh_token(refresh_token: str = Depends(check_cookie), user_dao: UserDAO = Depends()) -> TokenInfo:
#     if not refresh_token:
#         raise HTTPException(status_code=401, detail="No refresh token")
#     decoded_token = await decode_token(refresh_token, 'id', type='refresh')
#     if not decoded_token:
#         raise HTTPException(status_code=401, detail="Invalid refresh token")
#     user = get_user_by_id(db, decoded_token)
#     if not user:
#         raise HTTPException(status_code=401, detail="User does not exist")
#     access_token = create_access_token(data={"sub": user.email})
#     return JSONResponse({"token": access_token, "email": user.email}, status_code=200)
