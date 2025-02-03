from auth.auth import router as auth_router
from products.router import router as product_router
from storage.router import router as storage_router
from tasks import router as task_router
from users.router import router as user_router

endpoints_routers = (auth_router, product_router, storage_router, task_router, user_router)