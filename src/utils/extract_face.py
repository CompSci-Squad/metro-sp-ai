import base64
import io
from PIL import Image, ImageEnhance
import asyncio
import cv2
import cv2.data
import numpy as np
import face_recognition


async def extract_single_face_to_base64(base64_image: str):
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

    # Detect faces in the image using face_recognition
    face_locations = await asyncio.to_thread(face_recognition.face_locations, image_rgb)

    # Debugging: print the detected face locations
    print(f"Face locations: {face_locations}")

    # Handle cases with no faces or multiple faces
    if len(face_locations) == 0:
        raise ValueError("No face detected in the image.")
    elif len(face_locations) > 1:
        raise ValueError(f"Multiple faces detected: {len(face_locations)} faces found.")

   # If exactly one face is detected, extract it
    top, right, bottom, left = face_locations[0]
    face_image = image[top:bottom, left:right]  # Use 'image' here, not 'image_array'

    # Convert the face image (NumPy array) back to a PIL image
    face_image_pil = Image.fromarray(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))

    # Save the cropped face to a buffer
    buffer = io.BytesIO()
    await asyncio.to_thread(face_image_pil.save, buffer, format="JPEG")
    
    # Convert the buffer to base64 to return
    face_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return face_base64
