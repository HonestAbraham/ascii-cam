# 🎥 ASCII Cam

**ASCII Cam** is a real-time webcam filter that converts video frames into **ASCII art** directly in your terminal.  
It uses **OpenCV** for video capture and image processing, and **NumPy** for fast array manipulation.

---

## 🚀 Features
- 🖥️ Converts live webcam feed into ASCII art in real time  
- ⚙️ Adjustable resolution, gamma, and character sets  
- ✨ Edge-aware shading for better contrast  
- 💡 Works on Windows, macOS, and Linux terminals  
- ⚡ Built with efficient OpenCV + NumPy vectorization

---

## 🧩 Tech Stack

| Component | Purpose |
|------------|----------|
| **Python 3.11** | Core language |
| **OpenCV (`cv2`)** | Image capture and processing |
| **NumPy** | Fast pixel-wise math and array operations |
| **Blessed** *(optional)* | Flicker-free terminal rendering |
| **Pillow / Rich** *(optional)* | For future color or UI extensions |

---

## 🛠️ Installation (Windows, Python 3.11)

1. **Create and activate a virtual environment:**
   ```bash
   py -3.11 -m venv ascii_cam
   ascii_cam\Scripts\activate
