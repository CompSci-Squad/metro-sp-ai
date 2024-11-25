from fastapi import APIRouter
from .search_model import SearchModel
from ..database.client import client

search_router = APIRouter(prefix='/search')

@search_router.post('/')
async def search(payload: SearchModel):
    images = client.collections.get("Images")
    return await images.query.near_image(payload.image)