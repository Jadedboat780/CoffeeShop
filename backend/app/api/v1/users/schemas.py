from pydantic import BaseModel, EmailStr, Field, UUID4


class UserData(BaseModel):
    id: UUID4
    name: str
    surname: str
    email: EmailStr
    image: str | None = None


class GetUser(BaseModel):
    email: EmailStr
    password: str | bytes


class CreateUser(GetUser):
    name: str = Field(min_length=2, max_length=25)
    surname: str = Field(min_length=2, max_length=25)


class UpdateUserPartial(BaseModel):
    new_name: str | None = Field(min_length=2, max_length=25, default=None)
    new_surname: str | None = Field(min_length=2, max_length=25, default=None)
    new_email: EmailStr | None = None
    new_password: str | None = None
    new_image_url: str | None = None
