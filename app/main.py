from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    yield


app = FastAPI(**config.fastapi_args, lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_origin_regex=config.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=config.CORS_HEADERS,
)


@app.get("/debug/health", tags=["debug"])
async def debug() -> dict[str, str]:
    return {"status": "ok"}
