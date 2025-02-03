from pydantic import BaseModel
from typing import Annotated
from annotated_types import MinLen, MaxLen, Ge, Le

class CreateProduct(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(40)]
    price: Annotated[float, Ge(300), Le(500_000)]
    category: Annotated[str, MinLen(3), MaxLen(40)]
    description: Annotated[str | None, MinLen(30), MaxLen(150)] = None
    image_url: str

class GetProduct(CreateProduct):
    id: int


class UpdateProduct(CreateProduct):
    description: Annotated[str, MinLen(30), MaxLen(150)]

class UpdateProductPartial(BaseModel):
    title: Annotated[str | None, MinLen(3), MaxLen(40)] | None = None
    price: Annotated[float | None, Ge(300), Le(500_000)] = None
    category: Annotated[str | None, MinLen(3), MaxLen(40)] = None
    description: Annotated[str | None, MinLen(30), MaxLen(150)] = None
    image_url: str | None = None
