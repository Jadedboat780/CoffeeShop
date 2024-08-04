from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from contextlib import asynccontextmanager

from app.users import router as user_router
from app.products import router as product_router
from app.storage import router as storage_router
from app.tasks.product_sale import router as task_router
from app.auth import router as auth_router
from app.admin import create_admin, UserAdmin, ProductAdmin


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(title="Product Shop",
              docs_url="/documentation",
              default_response_class=ORJSONResponse,
              lifespan=lifespan)

# список источников, на которые разрешено выполнять кросс-доменные запросы
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ограничение количества запросов в минуту на api по ip
limiter = Limiter(key_func=get_remote_address, default_limits=["45/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# подключение роутеров
for router in (user_router, product_router, storage_router, auth_router, task_router):
    app.include_router(router)

admin = create_admin(app)
for view in (UserAdmin, ProductAdmin):
    admin.add_view(view)


@app.get("/", tags=["Hello word"], name="hello-world")
async def hello_word():
    """Приветственное сообщение"""

    return {"message": "Hello, world!"}
