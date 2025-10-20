# Import required libraries
import cv2, numpy as np, sys, time, os

# --- Settings ---
CAM_INDEX = 0  # Which webcam to use (0 = default camera)
# Full ASCII character set ordered from light to dark
CHARSET = np.array(list(" .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")) 
CELL_W, CELL_H = 6, 16  # Approximate width and height of one text character (affects aspect ratio)
TARGET_COLS = 200        # Number of ASCII characters (columns) across the screen
GAMMA = 1                # Gamma correction value (adjust brightness contrast)

# Function to clear the terminal between frames
def clear():
    # Works for both Windows and Unix-based terminals
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Capture video from webcam ---
cap = cv2.VideoCapture(CAM_INDEX)  # Open webcam using OpenCV
if not cap.isOpened():
    # Exit program if camera not found or not accessible
    print("Camera open failed")
    sys.exit(1)

try:
    while True:
        # Read one frame from webcam
        ok, frame = cap.read()
        if not ok:
            break  # Stop if frame capture fails

        # Convert captured frame to grayscale (drop color information)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)

        # --- Optional gamma correction (brightness/contrast tuning) ---
        if GAMMA != 1.0:
            # Adjust pixel brightness non-linearly to change perceived contrast
            gray = 255.0 * np.power(gray / 255.0, GAMMA)

        # --- Compute ASCII grid size based on aspect ratio ---
        h, w = gray.shape  # Image height and width in pixels
        cols = TARGET_COLS  # Desired number of character columns
        # Calculate how many rows we need to maintain image proportions
        # Adjust for the non-square shape of terminal characters
        rows = int((h / w) * cols * (CELL_W / CELL_H))
        rows = max(1, rows)  # Ensure at least one row

        # --- Downsample image to ASCII grid dimensions ---
        # Shrink image so each pixel roughly corresponds to one ASCII character
        small = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_AREA)

        # --- Optional edge detection to enhance shapes ---
        # Detect edges using Canny edge detector
        edges = cv2.Canny(gray.astype(np.uint8), 100, 200)
        # Downsample edges to same ASCII grid size
        edges_small = cv2.resize(edges, (cols, rows), interpolation=cv2.INTER_AREA) / 255.0

        # --- Normalize brightness to 0–1 range ---
        norm = np.clip(small, 0, 255) / 255.0
        # Scale brightness values to indices of CHARSET array
        idx = (norm * (len(CHARSET) - 1)).astype(np.int32)

        # --- Edge-based biasing (adds contrast around edges) ---
        edge_weight = 0.35  # How strongly to darken characters at edges
        # Add darker bias where edges are strong to emphasize shapes
        idx = np.clip(
            idx + (edges_small * edge_weight * (len(CHARSET) - 1)).astype(np.int32),
            0, len(CHARSET) - 1
        )

        # --- Define a smaller “ramp” of ASCII characters ---
        # This ramp has fewer characters and produces clearer contrast
        ramp = np.array(list(" .:-=+*#%@"), dtype="<U1")
        n = len(ramp)

        # --- Brightness → character mapping for smaller ramp ---
        # Convert normalized brightness values to character indices
        idx = (norm * (n - 1)).round().astype(np.int32)

        # --- Optional edge bias (re-applied for smaller ramp) ---
        edge_weight = 0.35  # Strength of edge-based darkening
        bias = (edges_small * edge_weight * (n - 1)).round().astype(np.int32)
        idx = np.clip(idx + bias, 0, n - 1)  # Keep valid index range

        # --- Map brightness indices to ASCII characters ---
        # Replace each pixel’s brightness with its corresponding ASCII character
        chars2d = ramp[idx]  # Create 2D array of characters matching image grid

        # --- Build printable ASCII rows ---
        # Join each row of characters into a single string line
        ascii_rows = ["".join(row) for row in chars2d]

        # --- Print ASCII art to terminal ---
        print("\n".join(ascii_rows))  # Display ASCII image

        # --- Clear terminal and print next frame ---
        clear()  # Clear screen to make animation smoother
        print("\n".join(ascii_rows))  # Print again after clear

        # --- Limit frame rate (~30 FPS) ---
        if cv2.waitKey(1) & 0xFF == 27:  # Stop if ESC key is pressed
            break

finally:
    # Release webcam when done
    cap.release()
