"""
Game Constants - enums and special values
"""
from enum import Enum

class GameState(Enum):
    """Represents different game states"""
    MENU = 1
    SETTINGS = 2
    IN_GAME = 3
    PAUSED = 4
    GAME_OVER = 5
    PLAYER_SCORED = 6  # Pause after player scores

class Difficulty(Enum):
    """AI Difficulty levels"""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

# Game outcome constants
PLAYER_WINS = 1
CPU_WINS = -1
NO_WINNER = 0
