from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timezone, timedelta
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict) -> str:
    '''Создания jwt access токена'''
    data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) # указываем время жизни для токена
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    '''Проверка валидности токена'''
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("username")
        return username
    except jwt.ExpiredSignatureError:  # обработка истечения срока жизни токена
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credential")
    # except jwt.InvalidTokenError: # обработка ошибки декодирования токена
    #     pass