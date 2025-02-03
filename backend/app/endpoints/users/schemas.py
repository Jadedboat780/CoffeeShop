from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import MinLen, MaxLen


class GetUser(BaseModel):
    email: EmailStr
    password: str


class CreateUser(GetUser):
    name: Annotated[str, MinLen(2), MaxLen(25)]
    surname: Annotated[str, MinLen(2), MaxLen(25)]


class UpdateUserPartial(BaseModel):
    name: Annotated[str | None, MinLen(2), MaxLen(25)] = None
    surname: Annotated[str | None, MinLen(2), MaxLen(25)] = None
    email: EmailStr | None = None
    password: str | None = None
    image_url: str | None = None
