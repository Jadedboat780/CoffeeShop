from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
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


class CoffeeCategory(StrEnum):
    cappuccino = auto()
    latte = auto()
    macchiato = auto()
    americano = auto()


class CoffeeSize(StrEnum):
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
    category: Mapped[CoffeeCategory]
    size: Mapped[CoffeeSize]
    image_url: Mapped[str | None] = mapped_column(String(50))
