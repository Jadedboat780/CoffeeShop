from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.products.router import router as product_router
from  app.users.router import router as user_router

app = FastAPI(title="Project", docs_url="/documentation")

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(user_router)

@app.get("/", tags=["Hello word"], name="hello-world")
async def root():
    return {"message": "Hello World"}

# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

