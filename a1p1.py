import cv2
import numpy as np

# Create a white canvas
img = np.ones((400, 400, 3), dtype=np.uint8) * 255

# Draw ellipses in Blue, Green, and Red
cv2.ellipse(img, (200, 120), (60, 100), 0, 0, 360, (255, 0, 0), -1)   # Blue ellipse (top)
cv2.ellipse(img, (120, 250), (60, 100), 0, 0, 360, (0, 255, 0), -1)   # Green ellipse (bottom left)
cv2.ellipse(img, (280, 250), (60, 100), 0, 0, 360, (0, 0, 255), -1)   # Red ellipse (bottom right)

# Add text "OpenCV" at the bottom center
cv2.putText(img, "OpenCV", (120, 380), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# Save the image
cv2.imwrite("opencv_logo.jpg", img)

# Display the image (optional for local testing)
cv2.imshow("OpenCV Logo", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
