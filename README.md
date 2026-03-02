# CV-Powered Snake Game with Low-Level Graphics

A modern take on the classic Snake game, powered by Computer Vision (Hand Tracking) and built using fundamental Computer Graphics (CG) algorithms from scratch.

## 🚀 Key Features

- **Word Building Challenge**: The snake now catches letters to form 3 and 4-letter words.
- **Sequential Spawning**: Letters appear one by one in the correct order for your target word.
- **Word-Based Scoring**: Your score increases for every complete word formed.
- **Wrap-Around Logic**: When the snake hits an edge, it seamlessly emerges from the opposite side.
- **Persistent High Score**: Tracks the maximum number of words completed in a session.

## 🎮 Controls

| Action | Control |
| :--- | :--- |
| **Move Snake** | Point your index finger at the screen (Webcam required) |
| **Restart Game** | Press **'R'** on your keyboard |
| **Exit Game** | Press **'ESC'** on your keyboard |

## 🛠️ Low-Level Computer Graphics Implementation

Unlike standard games that use high-level graphics libraries, this project implements core CG algorithms to render every pixel manually:

- **Bresenham's Line Algorithm**: Used to draw the grid lines and the game area boundary with pixel-perfect accuracy.
- **Scanline Fill Algorithm**: Used to color the snake's body segments by calculating horizontal spans for each block.
- **Cohen-Sutherland Clipping**: Grid lines are calculated for the full screen and then "clipped" to only display within the game arena using bit-coded region classification.
- **Pixel-By-Pixel Rendering**: Bypasses traditional high-level functions like `cv2.rectangle` for game elements to provide direct control over the image buffer.

## 📦 Installation & Setup

### Prerequisites
- Python 3.x
- Webcam

### Steps
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Snake_Game
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the game**:
   ```bash
   python main.py
   ```

## 📂 Project Structure

- `main.py`: Core game loop and CV integration.
- `bresenham.py`: Implementation of Bresenham's Line Algorithm.
- `fill.py`: Implementation of Scanline Fill Algorithm.
- `clipping.py`: Implementation of Cohen-Sutherland Clipping.

---
*Created as part of CGIP coursework.*
