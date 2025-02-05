from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from uuid import UUID, uuid4
from enum import StrEnum, auto


class User(SQLModel, table=True):
    """Users table"""

    __tablename__ = "users"

    id: UUID = Field(primary_key=True, default=uuid4)
    name: str = Field(max_length=25)
    surname: str = Field(max_length=25)
    email: EmailStr = Field(max_length=80, unique=True)
    password: bytes
    image_url: str | None = Field(max_length=100)


class Category(StrEnum):
    cappuccino = auto()
    latte = auto()
    macchiato = auto()
    americano = auto()


class CoffeSize(StrEnum):
    S = auto()
    M = auto()
    L = auto()


class Coffee(SQLModel, table=True):
    """Coffee table"""

    __tablename__ = "coffees"

    id: int = Field(primary_key=True)
    title: str = Field(min_length=20)
    description: str = Field(min_length=100)
    price: float = Field(min_length=50)
    category: Category
    size: CoffeSize
    image_url: str | None = Field(min_length=50)