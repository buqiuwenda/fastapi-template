from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="fastapi-agent", lifespan=lifespan)

app.include_router(api_router)
