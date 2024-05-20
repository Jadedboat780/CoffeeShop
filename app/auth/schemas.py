from pydantic import BaseModel


class TokenInfo(BaseModel):
    '''Информацию о токене'''
    access_token: str
    token_type: str