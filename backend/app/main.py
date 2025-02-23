from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.endpoints import endpoints_routers

@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(
    title="Coffee Shop",
    lifespan=lifespan
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connecting routers
for router in endpoints_routers:
    app.include_router(router)


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
