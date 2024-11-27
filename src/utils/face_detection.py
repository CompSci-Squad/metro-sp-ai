import base64
import io
from PIL import Image
import face_recognition
import asyncio

async def is_face_in_picture(base64_image: str) -> bool:
    image_data = await asyncio.to_thread(base64.b64decode, base64_image)
    image = await asyncio.to_thread(Image.open, io.BytesIO(image_data))
    image_array = await asyncio.to_thread(face_recognition.load_image_file, io.BytesIO(image_data))
    face_locations = await asyncio.to_thread(face_recognition.face_locations, image_array)

    if not face_locations:
        return False
    return True
