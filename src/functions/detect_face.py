from typing import Sequence
from numpy.typing import NDArray
import numpy as np
import cv2

ALG = "haarcascade_frontalface_default.xml"
# passing the algorithm to OpenCV
haar_cascade = cv2.CascadeClassifier(ALG)


def detect_face(np_image: NDArray[np.uint8]):
    img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    faces = haar_cascade.detectMultiScale(
        gray_img, scaleFactor=1.05, minNeighbors=2, minSize=(100, 100)
    )
    return faces