import logging
from fastapi import APIRouter, HTTPException
import weaviate.classes as wvc
from ..utils import extract_single_face_to_base64, is_face_in_picture
from weaviate.exceptions import WeaviateBaseError
from .search_model import SearchModel
from ..database.client import client

search_router = APIRouter(prefix='/search')
logger = logging.getLogger(__name__)

async def validate_face_image(image: str) -> str:
    if not await is_face_in_picture(image):
        raise HTTPException(status_code=400, detail="Image does not contain a face")
    return await extract_single_face_to_base64(image)

async def query_near_image(image: str):
    try:
        images = client.collections.get("Images")
        results = await images.query.near_image(near_image=image, return_metadata=wvc.query.MetadataQuery(distance=True, certainty=True))

        for obj in results.objects:
            distance = obj.metadata.distance
            if distance is not None and distance <= 0.2:
                return {
                    "recognized": True,
                    "message": "Face recognized with high certainty",
                    "cpf": obj.properties.get("cpf")
                }

        # If no matches meet the required distance threshold
        return {"recognized": False, "message": "Face not recognized"}
    except WeaviateBaseError as e:
        logger.error(f"Weaviate error: {e.message}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e.message}")

@search_router.post('/')
async def search(payload: SearchModel):
    try:
        if not payload or not payload.image:
            raise HTTPException(status_code=400, detail="Invalid payload: Image is required")

        validated_image = await validate_face_image(payload.image)

        return await query_near_image(validated_image)
    except HTTPException as e:
        logger.warning(f"HTTPException: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")