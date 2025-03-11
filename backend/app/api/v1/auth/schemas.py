from pydantic import BaseModel


class TokenInfo(BaseModel):
    """Information about the token"""
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
