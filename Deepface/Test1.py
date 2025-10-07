import torch
import torch.serialization
from hsemotion.facial_emotions import HSEmotionRecognizer
import cv2

# Fix for PyTorch 2.6+ weights_only loading issue: Add safe globals for model classes
# This allows secure loading of the pre-trained model without disabling security
try:
    from timm.models.efficientnet import EfficientNet
    from timm.layers.conv2d_same import Conv2dSame
    from timm.layers.norm_act import BatchNormAct2d
    torch.serialization.add_safe_globals([EfficientNet, Conv2dSame, BatchNormAct2d])
    print("Safe globals added successfully for model loading.")
except ImportError as e:
    print(f"Error: 'timm' or required modules not found. Install with 'pip install timm'. Details: {e}")
    exit()
except Exception as e:
    print(f"Error adding safe globals: {e}")
    exit()

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
if face_cascade.empty():
    print("Error: Could not load Haar Cascade classifier.")
    exit()

# Initialize HSEmotion recognizer (model will download on first run if not cached)
model_name = 'enet_b0_8_best_afew'
try:
    fer = HSEmotionRecognizer(model_name=model_name, device='cpu')
    print("HSEmotionRecognizer initialized successfully.")
except Exception as e:
    print(f"Error initializing HSEmotionRecognizer: {e}")
    exit()

# Start video capture from the default camera (0)
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Error: Could not open webcam.")
    exit()

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
        face_img = frame[y:y+h, x:x+w]
        # Ensure face_img is not empty
        if face_img.size > 0:
            try:
                emotion, scores = fer.predict_emotions(face_img, logits=False)
                score = max(scores) if scores else 0
                cv2.putText(frame, f'{emotion}: {score:.2f}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            except Exception as e:
                print(f"Error in emotion detection: {e}")

    # Display the frame with detected faces and emotions
    cv2.imshow("Capture", frame)

    # Wait for 1 millisecond and check for key press
    key = cv2.waitKey(1)

    # If 'q' is pressed, break the loop
    if key == ord('q'):
        break

# Print the total number of frames captured
print(f"Total frames captured: {a}")

# Release the video capture object and close all OpenCV windows
video.release()
cv2.destroyAllWindows()