from fastapi import APIRouter
from .search_model import SearchModel

search_router = APIRouter()

@search_router.post()
async def search(payload: SearchModel):
    