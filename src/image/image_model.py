from pydantic import BaseModel

class ImageModel(BaseModel):
    image: str
    cpf: str