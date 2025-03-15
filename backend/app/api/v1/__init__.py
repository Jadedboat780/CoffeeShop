from .auth.router import router as auth_router
from .coffees.router import router as coffees_router
from .users.router import router as user_router

api_routers = (auth_router, coffees_router, user_router)
