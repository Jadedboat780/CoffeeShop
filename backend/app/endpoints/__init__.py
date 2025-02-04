from pydantic import BaseModel
from typing import Annotated
from annotated_types import Ge

from auth.auth import router as auth_router
from products.router import router as product_router
from storage.router import router as storage_router
from tasks import router as task_router
from users.router import router as user_router


class Paginator(BaseModel):
    """Pagination model"""
    limit: Annotated[int, Ge(1)] = 100
    offset: Annotated[int, Ge(0)] = 0


endpoints_routers = (auth_router, product_router, storage_router, task_router, user_router)
