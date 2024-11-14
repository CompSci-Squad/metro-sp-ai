from fastapi import APIRouter

health_router = APIRouter(prefix='/health')


@health_router.get('/')
async def get_server_status():
    return {"status": "ok", "message": "Service is up and running!"}