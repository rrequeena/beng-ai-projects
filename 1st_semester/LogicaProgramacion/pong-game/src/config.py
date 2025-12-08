"""
Game Configuration
All constants and settings for the Pong game.
"""

# ============ DISPLAY SETTINGS ============
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "PONG Game"

# ============ COLORS ============
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_CYAN = (0, 255, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_RED = (220, 50, 50)
COLOR_DARK_RED = (180, 30, 30)

# ============ GAME PHYSICS ============
BALL_SIZE = 15
BALL_INITIAL_SPEED = 250  # pixels/second
BALL_MAX_SPEED = 500
BALL_MIN_SPEED = 200
SPEED_INCREMENT = 1.05  # 5% increase per paddle hit

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 400  # pixels/second
PADDLE_MARGIN = 30  # Distance from edge

# ============ GAME RULES ============
DEFAULT_WIN_POINTS = 10
MIN_WIN_POINTS = 1
MAX_WIN_POINTS = 50

# ============ AI SETTINGS ============
class AIDifficulty:
    EASY = 0.6      # 60% of max speed
    MEDIUM = 0.8    # 80% of max speed + error
    HARD = 0.95     # 95% of max speed + prediction

AI_REACTION_TIME = 0.1  # seconds - how often AI makes decisions
AI_PREDICTION_DISTANCE = 150  # pixels to look ahead for hard AI

# ============ VISUAL SETTINGS ============
FONT_LARGE = 72
FONT_MEDIUM = 48
FONT_SMALL = 24

CENTER_LINE_WIDTH = 2
CENTER_LINE_DASH = 10

# ============ ANIMATION ============
MENU_TRANSITION_TIME = 0.3  # seconds

