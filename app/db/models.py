from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

import uuid
from app.db.database import Base


class UserOrm(Base):
    """Таблица пользователей"""
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(25))
    surname: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[bytes]
    image_url: Mapped[str | None] = mapped_column(String(150))


class ProductOrm(Base):
    """Таблица товаров"""
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(40))
    price: Mapped[float]
    category: Mapped[str]
    description: Mapped[str | None] = mapped_column(String(150))
    image_url: Mapped[str] = mapped_column(String(50))

# class StoreOrm(Base):
#     ...
