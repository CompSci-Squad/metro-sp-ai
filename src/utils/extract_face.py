import base64
import io
from PIL import Image
import face_recognition
import asyncio

async def extract_single_face_to_base64(base64_image: str):
    image_data = await asyncio.to_thread(base64.b64decode, base64_image)
    image = await asyncio.to_thread(Image.open, io.BytesIO(image_data))
    image_array = await asyncio.to_thread(face_recognition.load_image_file, io.BytesIO(image_data))
    face_locations = await asyncio.to_thread(face_recognition.face_locations, image_array)

    if len(face_locations) != 1:
        raise ValueError("The image must contain exactly one face.")

    top, right, bottom, left = face_locations[0]
    face_image = image.crop((left, top, right, bottom))
    buffer = io.BytesIO()
    await asyncio.to_thread(face_image.save, buffer, format="JPEG")
    face_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return face_base64
