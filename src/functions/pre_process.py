import base64
import numpy as np
from numpy.typing import NDArray

def decode_base64(base64_image: str)-> NDArray[np.uint8]:
    image_data = base64.b64decode(base64_image)

    return np.frombuffer(image_data, np.uint8)