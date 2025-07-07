import cv2
import numpy as np

# Initialize video capture from the default webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set camera properties: width, height, and brightness
cap.set(3, 1080)  # Width
cap.set(4, 720)   # Height
cap.set(10, 100)  # Brightness

# Make the display window resizable
cv2.namedWindow("Color Detection", cv2.WINDOW_NORMAL)

while True:
    # Capture a frame from the webcam
    success, img = cap.read()
    if not success:
        print("Failed to capture frame")
        continue

    # Convert the frame from BGR to HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get frame dimensions
    height, width, _ = img.shape

    # Calculate the center point
    cx = int(width / 2)
    cy = int(height / 2)

    # Draw a green circle at the center to indicate detection point
    cv2.circle(img, (cx, cy), 10, (0, 255, 0), 2)

    # Get HSV values at the center pixel
    hsv_center = hsv_img[cy, cx]
    hue_val = hsv_center[0]

    # Determine color based on hue value
    color = "Undefined"
    if hue_val < 5:
        color = "RED"
    elif hue_val < 22:
        color = "ORANGE"
    elif hue_val < 33:
        color = "YELLOW"
    elif hue_val < 78:
        color = "GREEN"
    elif hue_val < 131:
        color = "BLUE"
    elif hue_val < 170:
        color = "VIOLET"
    else:
        color = "RED"  # Hue values near 180 wrap around to red

    # Define a centered rectangle for displaying the color name
    rect_width = 420
    rect_height = 110
    rect_x = int(width / 2 - rect_width / 2)
    rect_y = 10

    # Draw a white filled rectangle
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (255, 255, 255), -1)

    # Display the color name in black text for readability
    text_x = rect_x + 10
    text_y = rect_y + 80
    cv2.putText(img, color, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

    # Show the frame
    cv2.imshow("Color Detection", img)

    # Exit the loop if the window is closed
    if cv2.getWindowProperty("Color Detection", cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()