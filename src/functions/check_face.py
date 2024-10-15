import face_recognition

def check_face(image1_path):
    # Load the first image
    image1 = face_recognition.load_image_file(image1_path)
    image1_encodings = face_recognition.face_encodings(image1)

    if len(image1_encodings) == 0:
        return "No face found in the first image."
    else: 
        return 'Found Face in image'
