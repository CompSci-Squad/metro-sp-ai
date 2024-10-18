# importing the cv2 library
import base64
import os
import cv2
from .functions.pre_process import decode_base64
from .functions.detect_face import detect_face

# # loading the haar case algorithm file into alg variable
# alg = "haarcascade_frontalface_default.xml"
# # passing the algorithm to OpenCV
# haar_cascade = cv2.CascadeClassifier(alg)
# # loading the image path into file_name variable - replace <INSERT YOUR IMAGE NAME HERE> with the path to your image
# file_name = "test-image.png"
# # reading the image
# img = cv2.imread(file_name, 0)
# # creating a black and white version of the image
# gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
# # detecting the faces
# faces = haar_cascade.detectMultiScale(
#     gray_img, scaleFactor=1.05, minNeighbors=2, minSize=(100, 100)
# )

# i = 0
# # for each face detected
# for x, y, w, h in faces:
#     # crop the image to select only the face
#     cropped_image = img[y : y + h, x : x + w]
#     # loading the target image path into target_file_name variable  - replace <INSERT YOUR TARGET IMAGE NAME HERE> with the path to your target image
#     target_file_name = 'stored-faces/' + str(i) + '.jpg'
#     cv2.imwrite(
#         target_file_name,
#         cropped_image,
#     )
#     i = i + 1

def main():
    image_path = os.path.join(os.path.dirname(__file__), '../images/image_test1.jpeg')
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    #   Encode the image as a JPEG (or PNG) byte array
    _, buffer = cv2.imencode('.jpg', image)

    # Convert the byte array to base64
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    print(detect_face(decode_base64(encoded_image)))
    


if __name__ == '__main__':
    main()