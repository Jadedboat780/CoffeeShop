from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
import uuid
from pydantic import EmailStr
from enum import StrEnum, auto
from .database import Base


class UserOrm(Base):
    """Users table"""
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(25))
    surname: Mapped[str] = mapped_column(String(25))
    email: Mapped[EmailStr] = mapped_column(String(50), unique=True)
    password: Mapped[bytes]
    image_url: Mapped[str | None] = mapped_column(String(150))


class Category(StrEnum):
    cappuccino = auto()
    latte = auto()
    macchiato = auto()
    americano = auto()


class CoffeSize(StrEnum):
    S = auto()
    M = auto()
    L = auto()


class CoffeeOrm(Base):
    """Coffee table"""
    __tablename__ = "coffees"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(100))
    price: Mapped[float]
    category: Mapped[Category]
    size: Mapped[CoffeSize]
    image_url: Mapped[str | None] = mapped_column(String(50))
