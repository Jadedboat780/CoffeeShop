from pydantic import BaseModel
from typing import Annotated
from annotated_types import Ge


class Paginator(BaseModel):
    """Плагинация"""
    limit: Annotated[int, Ge(1)] = 100
    offset: Annotated[int, Ge(0)] = 0
