from fastapi import APIRouter, HTTPException
from .image_model import ImageModel
from ..database.client import client
from weaviate.exceptions import WeaviateBaseError, ObjectAlreadyExistsError

image_router = APIRouter(prefix='/image')

@image_router.post('/')
async def add_image(payload: ImageModel):
    try: 
        images = client.collections.get("Images")
        await images.data.insert({
            'image': payload.image,
            'cpf': payload.cpf
        })
        return {'message': 'Created image'}
    except ObjectAlreadyExistsError as e:
        raise HTTPException(400, detail='object already exists')
    except WeaviateBaseError as e:
        raise HTTPException(500, detail=f'internal server error, error: {e.message}')