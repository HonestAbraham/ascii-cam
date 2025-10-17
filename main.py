import cv2
import numpy as np

TEST_IMAGE_FILE_PATH = "image_check/test_image_1.jpg"
CELL_W, CELL_H = 6, 16         # match terminal character geometry
TARGET_COLS = 200              # number of characters across

img = cv2.imread(TEST_IMAGE_FILE_PATH)   
if img is None:
    raise SystemExit("Couldn't load ", TEST_IMAGE_FILE_PATH, " — put an image next to this script.")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Calculates how many text rows your ASCII output should have
# Each character cell roughly corresponds to a rectangle of size CELL_W × CELL_H pixels (e.g., 6×16)
h, w = gray.shape
rows = max(1, int((h / w) * TARGET_COLS * (CELL_W / CELL_H)))

# Downsample to (cols, rows) 
# Interpolation is the mathematical rule it uses to decide what color or brightness each new pixel should have.
# INTER_AREA just means downsizing. Different macros are for different things, for example INTER_CUBIC for high quality enlarging
small = cv2.resize(gray, (TARGET_COLS, rows), interpolation=cv2.INTER_AREA)

print(f"Original size: {w}x{h}")
print(f"Resized for ASCII grid: {TARGET_COLS}x{rows}")
print(small.shape)

cv2.imshow("Original", img)
cv2.imshow("Grayscale", gray)
cv2.imshow("Downsampled", cv2.resize(small, (TARGET_COLS*4, rows*8), interpolation=cv2.INTER_NEAREST))
cv2.waitKey(0)
cv2.destroyAllWindows()
