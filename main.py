from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.products.router import router as product_router
from app.users.router import router as user_router
from app.tasks.product_sale import router as task_router
from app.auth.auth import router as auth_router
from app.file import router as file_router
from app.config import settings

app = FastAPI(title="Project", docs_url="/documentation")

# список источников, на которые разрешено выполнять кросс-доменные запросы
origins = [
    "http://localhost",
    "http://localhost:8080"
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
app.include_router(product_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(file_router)
app.include_router(task_router)

@app.get("/", tags=["Hello word"], name="hello-world")
async def root():
    '''Приветственное сообщение'''
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup_event():
    '''Подключение к redis'''
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")