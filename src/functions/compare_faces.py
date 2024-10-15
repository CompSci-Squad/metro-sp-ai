import face_recognition

def compare_faces(image1_path, image2_path):
    # Load the first image
    image1 = face_recognition.load_image_file(image1_path)
    image1_encodings = face_recognition.face_encodings(image1)

    if len(image1_encodings) == 0:
        return "No face found in the first image."

    # Load the second image
    image2 = face_recognition.load_image_file(image2_path)
    image2_encodings = face_recognition.face_encodings(image2)

    if len(image2_encodings) == 0:
        return "No face found in the second image."

    # Compare faces
    results = face_recognition.compare_faces([image1_encodings[0]], image2_encodings[0])

    if results[0]:
        return "Faces match!"
    else:
        return "Faces do not match."