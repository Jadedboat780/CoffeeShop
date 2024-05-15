from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class ProductOrm(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(40))
    price: Mapped[float]
    description: Mapped[str | None] = mapped_column(String(150))


class UserOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    surname: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[bytes]
