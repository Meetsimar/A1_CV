import cv2
import numpy as np

# Create a white background
img = np.ones((400, 400, 3), dtype=np.uint8) * 255

# Circle settings
radius = 60
thickness = 35

# Positions
red_center = (200, 110)
green_center = (120, 260)
blue_center = (280, 260)

# Draw 3 hollow circles
cv2.circle(img, red_center, radius, (0, 0, 255), thickness)     # Red
cv2.circle(img, green_center, radius, (0, 255, 0), thickness)   # Green
cv2.circle(img, blue_center, radius, (255, 0, 0), thickness)    # Blue

# Create flat cutouts using white triangles
# Red cutout (top)
cv2.fillPoly(img, [np.array([
    [red_center[0] - 40, red_center[1] + 80],
    [red_center[0] + 40, red_center[1] + 80],
    [red_center[0],       red_center[1]]
])], (255, 255, 255))

# Green cutout (bottom)
cv2.fillPoly(img, [np.array([[green_center[0]+60, green_center[1]-90],
                             [green_center[0]+100, green_center[1]-60],
                             [green_center[0], green_center[1]]])], (255, 255, 255))

# Blue cutout (bottom)
cv2.fillPoly(img, [np.array([[blue_center[0]-40, blue_center[1]-80],
                             [blue_center[0]+40, blue_center[1]-80],
                             [blue_center[0], blue_center[1]]])], (255, 255, 255))

# Add OpenCV text
cv2.putText(img, "OpenCV", (125, 380), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# Save and show
cv2.imwrite("opencv_logo_no_ellipse.jpg", img)
cv2.imshow("OpenCV Logo", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

