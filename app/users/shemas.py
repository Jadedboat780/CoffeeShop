from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import MinLen, MaxLen


class CreateUser(BaseModel):
    name: Annotated[str, MinLen(2), MaxLen(25)]
    surname: Annotated[str, MinLen(2), MaxLen(25)]
    email: EmailStr
    password: bytes


class GetUser(CreateUser):
    id: int


class UpdateUser(CreateUser):
    pass


class UpdateUserPartial(CreateUser):
    name: Annotated[str | None, MinLen(2), MaxLen(25)] = None
    surname: Annotated[str | None, MinLen(2), MaxLen(25)] = None
    email: EmailStr | None = None
    password: bytes | None = None
