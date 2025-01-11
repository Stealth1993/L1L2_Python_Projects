import cv2
from deepface import DeepFace

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start video capture from the default camera (0)
video = cv2.VideoCapture(0)

a = 0  # Counter for frames

while True:
    a += 1  # Increment frame counter
    check, frame = video.read()  # Read a frame from the video capture

    # Check if the frame was captured successfully
    if not check:
        print("Failed to capture frame")
        break

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangles around the detected faces and detect emotions
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face = frame[y:y+h, x:x+w]
        result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
        # Modification: Access the first element of the result list
        if result:
            emotion = result[0]['dominant_emotion']
            score = result[0]['emotion'][emotion]
            if emotion:
                cv2.putText(frame, f'{emotion}: {score:.2f}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Display the frame with detected faces and emotions
    cv2.imshow("Capture", frame)

    # Wait for 1 millisecond and check for key press
    key = cv2.waitKey(1)

    # If 'q' is pressed, break the loop
    if key == ord('q'):
        break

# Print the total number of frames captured
print(a)

# Release the video capture object and close all OpenCV windows
video.release()
cv2.destroyAllWindows()