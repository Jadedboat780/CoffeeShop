from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from endpoints import endpoints_routers
from admin import create_admin, UserAdmin, ProductAdmin


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(
    title="Product Shop",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

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

# подключение роутеров
for router in endpoints_routers:
    app.include_router(router)

admin = create_admin(app)
for view in (UserAdmin, ProductAdmin):
    admin.add_view(view)


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
