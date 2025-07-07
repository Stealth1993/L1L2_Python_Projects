import cv2
import numpy as np

# Initialize video capture from the default webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set resolution to 640x480 for better performance
cap.set(3, 640)
cap.set(4, 480)

# Create a resizable window
cv2.namedWindow("Color Detection", cv2.WINDOW_NORMAL)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame")
        continue

    # Get frame dimensions
    height, width, _ = img.shape
    cx = int(width / 2)
    cy = int(height / 2)

    # Draw a green circle at the center to indicate detection point
    cv2.circle(img, (cx, cy), 10, (0, 255, 0), 2)

    # Get the center pixel in BGR
    pixel_bgr = img[cy, cx]
    # Reshape to 1x1x3 and convert to HSV for efficiency
    pixel_bgr_reshaped = pixel_bgr.reshape(1,1,3)
    pixel_hsv = cv2.cvtColor(pixel_bgr_reshaped, cv2.COLOR_BGR2HSV)
    hue_val = pixel_hsv[0,0,0]

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

    # Check if the window is closed
    if cv2.getWindowProperty("Color Detection", cv2.WND_PROP_VISIBLE) < 1:
        print("Window closed, exiting...")
        break

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()