from pydantic import BaseModel, Field

from app.db.models import CoffeeCategory, CoffeeSize


class CreateCoffee(BaseModel):
    title: str = Field(min_length=3, max_length=20)
    description: str = Field(min_length=30, max_length=100)
    price: float = Field(ge=50, le=5_000)
    category: CoffeeCategory
    size: CoffeeSize
    image_url: str | None = None


class GetCoffee(CreateCoffee):
    id: int = Field(ge=1)


class UpdateCoffee(CreateCoffee): ...


class UpdateCoffeePartial(BaseModel):
    title: str | None = Field(min_length=3, max_length=20, default=None)
    description: str | None = Field(min_length=30, max_length=100, default=None)
    price: float | None = Field(ge=50, le=5_000, default=None)
    category: CoffeeCategory | None = None
    size: CoffeeSize | None = None
    image_url: str | None = None
