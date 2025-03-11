from typing import Any

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timezone, timedelta
from app.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(subject: str | Any) -> str:
    """Create access jwt token"""
    access_expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_payload = {"sub": str(subject), "exp": access_expire, "type": "access"}
    access_token = jwt.encode(access_payload, config.SECRET_KEY, algorithm=config.ALGORITHM)

    return access_token


def create_refresh_token(subject: str | Any) -> str:
    """Create refresh jwt token"""
    refresh_expire = datetime.now(timezone.utc) + timedelta(days=config.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_payload = {"sub": str(subject), "exp": refresh_expire, "type": "refresh"}
    refresh_token = jwt.encode(refresh_payload, config.SECRET_KEY, algorithm=config.ALGORITHM)

    return refresh_token


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        print(payload)
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.InvalidTokenError:
        raise None
    # HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Could not validate credential")
