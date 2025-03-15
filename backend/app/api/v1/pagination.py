from typing import Annotated

from annotated_types import Ge
from pydantic import BaseModel


class Paginator(BaseModel):
    """Pagination model"""

    limit: Annotated[int, Ge(1)] = 100
    offset: Annotated[int, Ge(0)] = 0
