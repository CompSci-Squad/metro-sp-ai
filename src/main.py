from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
import signal
from .database.client import client
from .database.schema import generate_schema
from .health import health_router
from .search import search_router
from .image import image_router
from .config import Settings

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

def main():
    config = Settings()
    print(config.model_dump_json())
    loop = asyncio.get_event_loop()
    stop_event = asyncio.Event()


    loop.add_signal_handler(signal.SIGINT, stop_event.set)

    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=config.port, loop="asyncio")
    server = uvicorn.Server(config)

    try:
        loop.run_until_complete(asyncio.gather(server.serve(), stop_event.wait()))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

if __name__ == "__main__":
    main()