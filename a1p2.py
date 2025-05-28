import cv2
import numpy as np

def manual_blend_images(img1_path, img2_path, alpha, output_path="manual_blend.jpg"):
    # Read images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # Resize second image to match the first image
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Ensure the images are in float format for blending
    img1_float = img1.astype(np.float32)
    img2_float = img2.astype(np.float32)

    # Perform manual blending
    blended = (1 - alpha) * img1_float + alpha * img2_float
    blended = np.clip(blended, 0, 255).astype(np.uint8)

    # Save the blended image
    cv2.imwrite(output_path, blended)
    print(f"Blended image saved as {output_path}")


manual_blend_images("./cat.jpeg", "./tree.jpeg", 0.5)
