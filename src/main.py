from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from .database.client import client
from .database.schema import generate_schema
from .health import health_router
from .search import search_router
from .image import image_router
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.connect()
    await generate_schema()
    yield
    await client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(search_router)
app.include_router(image_router)

if __name__ == "__main__":
    uvicorn.run(app)
