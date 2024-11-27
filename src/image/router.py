import logging
from fastapi import APIRouter, HTTPException
from .image_model import ImageModel
from ..database.client import client
from ..utils import is_face_in_picture, extract_single_face_to_base64
from weaviate.exceptions import WeaviateBaseError, ObjectAlreadyExistsError

image_router = APIRouter(prefix='/image')

logger = logging.getLogger(__name__)

async def validate_face_image(image: str) -> str:
    if not await is_face_in_picture(image):
        raise HTTPException(status_code=400, detail="Image does not contain a face")
    return await extract_single_face_to_base64(image)

async def insert_image_to_collection(image: str, cpf: str):
    try:
        images = client.collections.get("Images")
        await images.data.insert({'image': image, 'cpf': cpf})
    except ObjectAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Object already exists")
    except WeaviateBaseError as e:
        logger.error(f"Weaviate error: {e.message}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e.message}")

@image_router.post('/', status_code=201)
async def add_image(payload: ImageModel):
    try:
        if not payload or not payload.image or not payload.cpf:
            raise HTTPException(status_code=400, detail="Invalid payload")

        image = await validate_face_image(payload.image)
        await insert_image_to_collection(image, payload.cpf)

        return {"message": "Created image"}
    except HTTPException as e:
        logger.warning(f"HTTPException: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
