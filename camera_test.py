import cv2

# 1. Initialize the camera (0 is usually your default laptop webcam)
cap = cv2.VideoCapture(0)

# 2. The Capture Loop
while True:
    # Read a single frame from the camera
    success, frame = cap.read()
    
    # If the camera fails to grab a frame, skip to the next iteration
    if not success:
        print("Failed to grab frame.")
        break
        
    # Flip the frame horizontally so it acts like a mirror (feels more natural)
    frame = cv2.flip(frame, 1)

    # 3. Display the frame in a window named "Camera Feed"
    cv2.imshow("Camera Feed", frame)

    # 4. Exit condition: Wait 1 millisecond for the 'q' key to be pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. Cleanup: Release the camera and close the window
cap.release()
cv2.destroyAllWindows()