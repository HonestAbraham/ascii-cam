import cv2, numpy as np, sys, time, os

# --- Settings ---
CAM_INDEX = 0
CHARSET = np.array(list(" .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")) 
CELL_W, CELL_H = 6, 16              
TARGET_COLS = 200                   # tweak depending on your terminal width
GAMMA = 1                            # try 0.9–1.2

def clear():
    # works in most terminals
    os.system('cls' if os.name == 'nt' else 'clear')

cap = cv2.VideoCapture(CAM_INDEX)
if not cap.isOpened():
    print("Camera open failed"); sys.exit(1)

try:
    while True:
        ok, frame = cap.read()
        if not ok: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)

        # gamma correction (optional)
        if GAMMA != 1.0:
            gray = 255.0 * np.power(gray/255.0, GAMMA)

        h, w = gray.shape
        # compute rows from cols and cell aspect
        cols = TARGET_COLS
        rows = int((h / w) * cols * (CELL_W / CELL_H))
        rows = max(1, rows)

        # resize to character grid dimensions
        small = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_AREA)

        # optional edge-aware tweak
        # compute edge density at a coarser scale to bias mapping
        edges = cv2.Canny(gray.astype(np.uint8), 100, 200)
        edges_small = cv2.resize(edges, (cols, rows), interpolation=cv2.INTER_AREA) / 255.0

        # normalize brightness to 0..len(CHARSET)-1
        norm = np.clip(small, 0, 255) / 255.0
        idx = (norm * (len(CHARSET) - 1)).astype(np.int32)

        # bias with edges: push toward darker chars in edgey cells
        # tune weight 0..0.5 (more edge -> darker symbol)
        edge_weight = 0.35
        idx = np.clip(idx + (edges_small * edge_weight * (len(CHARSET)-1)).astype(np.int32),
                      0, len(CHARSET)-1)
                
        ramp = np.array(list(" .:-=+*#%@"), dtype="<U1")   # ASCII ramp
        n = len(ramp)

        # brightness -> index
        idx = (norm * (n - 1)).round().astype(np.int32)

        # optional edge bias (push “edgier” cells darker)
        edge_weight = 0.35  # 0..0.5 is typical
        bias = (edges_small * edge_weight * (n - 1)).round().astype(np.int32)
        idx = np.clip(idx + bias, 0, n - 1)  # keep indices valid

        # map indices -> characters (2D array of shape [rows, cols])
        chars2d = ramp[idx]                  # no extra indexing!

        # build lines for the terminal
        ascii_rows = ["".join(row) for row in chars2d]     # <-- key fix
        print("\n".join(ascii_rows))

        clear()
        print("\n".join(ascii_rows))

        # ~30 FPS max (depends on terminal)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break
finally:
    cap.release()
