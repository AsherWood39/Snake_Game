import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector
import cvzone
from bresenham import bresenham_line
from fill import scanline_fill
from clipping import cohen_sutherland

GRID_SIZE = 20  # size of one block in pixels
WIDTH, HEIGHT = 1280, 720
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)
detector = HandDetector(detectionCon=0.8, maxHands=1)

def draw_pixels(img, points, color):
    """Draw points pixel-by-pixel on the image"""
    for x, y in points:
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            img[int(y), int(x)] = color

class SnakeGameGrid:
    def __init__(self, high_score=0):
        self.margin = 100
        self.grid_width = (WIDTH - 2 * self.margin) // GRID_SIZE
        self.grid_height = (HEIGHT - 2 * self.margin) // GRID_SIZE
        self.snake = [(self.grid_width//2, self.grid_height//2)]
        self.direction = (1, 0) # Start moving right
        self.spawn_food()
        self.score = 0
        self.high_score = high_score
        self.last_move_time = cv2.getTickCount()
        self.move_delay = 0.52 # Adjust for speed (increased for easier control)
        self.last_food_time = cv2.getTickCount()
        self.food_timer = 120 # 2 minutes in seconds
        self.game_over = False
        self.words = ["CAT", "DOG", "SUN", "MOON", "FISH", "STAR", "BIRD", "TREE", "BOOK", "RAIN", "SNOW", "FIRE"]
        self.target_word = ""
        self.current_word_letters = []
        self.total_words_completed = 0
        self.reset_word()

    def reset_word(self):
        self.target_word = random.choice(self.words)
        self.current_word_letters = []
        self.spawn_food()

    def spawn_food(self):
        while True:
            self.food = (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
            if self.food not in self.snake:
                self.last_food_time = cv2.getTickCount()
                break

    def get_current_letter(self):
        if len(self.current_word_letters) < len(self.target_word):
            return self.target_word[len(self.current_word_letters)]
        return ""

    def update(self, hand_pos):
        if self.game_over:
            return True

        # Update direction based on hand position relative to the head
        if hand_pos is not None:
            head = self.snake[0]
            # Map screen hand pos to grid pos relative to margin
            gx = (hand_pos[0] - self.margin) // GRID_SIZE
            gy = (hand_pos[1] - self.margin) // GRID_SIZE
            
            dx = gx - head[0]
            dy = gy - head[1]

            # Choose direction towards the hand (prioritizing current axis or simple distance)
            if abs(dx) > abs(dy):
                self.direction = (1 if dx > 0 else -1, 0)
            elif abs(dy) > abs(dx):
                self.direction = (0, 1 if dy > 0 else -1)

        # Check food timer
        now = cv2.getTickCount()
        freq = cv2.getTickFrequency()
        if (now - self.last_food_time) / freq > self.food_timer:
            self.spawn_food()

        # Regular movement based on time
        if (now - self.last_move_time) / freq > self.move_delay:
            self.last_move_time = now
            head = self.snake[0]
            # Move snake by wrapping around the game area
            new_head = ((head[0] + self.direction[0]) % self.grid_width, 
                        (head[1] + self.direction[1]) % self.grid_height)

            # Check self collision
            if new_head in self.snake:
                self.game_over = True
                return False
            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.current_word_letters.append(self.get_current_letter())
                if len(self.current_word_letters) == len(self.target_word):
                    self.score += 1 # Score based on words completed
                    self.total_words_completed += 1
                    self.reset_word()
                else:
                    self.spawn_food()
            else:
                self.snake.pop()

        return True

    def draw(self, img, webcam_img):
        viewport = (self.margin, self.margin, WIDTH - self.margin, HEIGHT - self.margin)

        # Draw game area boundary using Bresenham's Line
        boundary_points = []
        boundary_points.extend(bresenham_line(self.margin, self.margin, WIDTH - self.margin, self.margin))
        boundary_points.extend(bresenham_line(WIDTH - self.margin, self.margin, WIDTH - self.margin, HEIGHT - self.margin))
        boundary_points.extend(bresenham_line(WIDTH - self.margin, HEIGHT - self.margin, self.margin, HEIGHT - self.margin))
        boundary_points.extend(bresenham_line(self.margin, HEIGHT - self.margin, self.margin, self.margin))
        draw_pixels(img, boundary_points, (255, 255, 255))

        # Draw grid background using Bresenham's Line and Cohen-Sutherland Clipping
        grid_points = []
        for x in range(0, WIDTH, GRID_SIZE):
            clipped = cohen_sutherland(x, 0, x, HEIGHT, viewport)
            if clipped:
                grid_points.extend(bresenham_line(int(clipped[0]), int(clipped[1]), int(clipped[2]), int(clipped[3])))
        for y in range(0, HEIGHT, GRID_SIZE):
            clipped = cohen_sutherland(0, y, WIDTH, y, viewport)
            if clipped:
                grid_points.extend(bresenham_line(int(clipped[0]), int(clipped[1]), int(clipped[2]), int(clipped[3])))
        draw_pixels(img, grid_points, (50, 50, 50))

        # Draw current target letter using custom text rendering
        fx, fy = self.food
        letter = self.get_current_letter()
        cx = self.margin + fx * GRID_SIZE + GRID_SIZE // 2
        cy = self.margin + fy * GRID_SIZE + GRID_SIZE // 2
        
        # We'll use cv2.putText for the letter as pixel-perfect fonts from scratch are complex
        # but we draw it on our pixel-based buffer
        cv2.putText(img, letter, (cx - 7, cy + 7), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Draw snake using Scanline Fill
        for i, (x, y) in enumerate(self.snake):
            color = (0, 255, 0) if i == 0 else (0, 180, 0)
            x1, y1 = self.margin + x * GRID_SIZE, self.margin + y * GRID_SIZE
            x2, y2 = x1 + GRID_SIZE, y1 + GRID_SIZE
            
            # Rectangle vertices for scanline fill
            rect_poly = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
            segment_points = scanline_fill(rect_poly, WIDTH)
            draw_pixels(img, segment_points, color)

        # Draw scores and current word progress
        cvzone.putTextRect(img, f'WORDS: {self.total_words_completed}', [20, 50], scale=2, thickness=2, offset=10)
        cvzone.putTextRect(img, f'HI-WORDS: {self.high_score}', [WIDTH - 350, 50], scale=2, thickness=2, offset=10)
        
        # Show target word progress
        progress = "".join(self.current_word_letters)
        target = self.target_word
        cvzone.putTextRect(img, f'WORD: {progress} / {target}', [WIDTH // 2 - 150, 50], scale=2, thickness=2, offset=10, colorR=(100, 100, 0))

        # Draw small webcam preview bottom right
        small_cam = cv2.resize(webcam_img, (160, 120))
        img[HEIGHT - 130:HEIGHT - 10, WIDTH - 170:WIDTH - 10] = small_cam
        if self.game_over:
            cvzone.putTextRect(img, "GAME OVER", [400, 300], scale=5, thickness=5, offset=20)
            cvzone.putTextRect(img, f'Final Score: {self.score}', [450, 400], scale=3, thickness=3, offset=20)
            cvzone.putTextRect(img, "Press 'R' to Restart", [420, 500], scale=2, thickness=2, offset=10)
            
        return img

game = SnakeGameGrid()
while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)  # mirror image for natural movement
    hands, img = detector.findHands(img, flipType=False)
    hand_pos = None
    if hands:
        lmList = hands[0]["lmList"]
        hand_pos = lmList[8][0:2]
    cv2.circle(img, hand_pos, 30, (255, 0, 255), cv2.FILLED)
    if not game.update(hand_pos):
        # Game over state handled within update, but we ensure high score is ready
        if game.game_over:
            game.high_score = max(game.score, game.high_score)
    # Create a solid black background
    game_img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    img = game.draw(game_img, img)
    cv2.imshow("Snake Grid", img)
    key = cv2.waitKey(1)
    if key == ord('r') or key == ord('R'):
        game = SnakeGameGrid(high_score=game.high_score)
    if key == 27:  # ESC to quit
        break
cap.release()
cv2.destroyAllWindows()