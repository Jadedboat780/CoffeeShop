
# from .auth.auth import router as auth_router
from .coffees.router import router as coffees_router
# from .storage.router import router as storage_router
# from .tasks import router as task_router
from .users.router import router as user_router




endpoints_routers = (coffees_router, user_router)
