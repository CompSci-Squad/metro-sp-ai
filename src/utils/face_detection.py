import base64
import io
from PIL import Image, ImageEnhance
import face_recognition
import asyncio
import cv2
import numpy as np

async def is_face_in_picture(base64_image: str) -> bool:
    try:
        # Decode the base64 image
        image_data = await asyncio.to_thread(base64.b64decode, base64_image)

        # Convert to a NumPy array
        image_np = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # Enhance brightness and contrast
        alpha = 1.5  # Contrast control
        beta = 50    # Brightness control
        image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

        # Resize to improve detection
        image = cv2.resize(image, (image.shape[1] * 2, image.shape[0] * 2))

        # Convert to RGB for face_recognition
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = await asyncio.to_thread(face_recognition.face_locations, image_rgb)
        return bool(face_locations)

    except Exception as e:
        raise ValueError(f"Error processing image: {e}")