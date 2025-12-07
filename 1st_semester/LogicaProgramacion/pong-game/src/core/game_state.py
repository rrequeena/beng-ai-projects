"""
Game State Manager
SOLID: Single Responsibility - State transitions only
Design Pattern: State Pattern
"""
from src.utils.constants import GameState, Difficulty

class GameStateManager:
    """
    Manages game state and transitions
    
    States:
    - MENU: Main menu
    - SETTINGS: Choose difficulty and win points
    - IN_GAME: Active game
    - PAUSED: Game paused
    - GAME_OVER: Game ended
    """
    
    def __init__(self):
        """Initialize state manager"""
        self.current_state = GameState.MENU
        self.previous_state = None
        self.win_points = 10
        self.difficulty = Difficulty.MEDIUM.value
    
    def transition_to(self, new_state: GameState) -> None:
        """
        Change game state with validation
        
        Args:
            new_state: Target game state
        """
        self.previous_state = self.current_state
        self.current_state = new_state
    
    def is_in_game(self) -> bool:
        """Check if currently playing"""
        return self.current_state == GameState.IN_GAME
    
    def is_in_menu(self) -> bool:
        """Check if in menu"""
        return self.current_state == GameState.MENU
    
    def set_difficulty(self, difficulty: Difficulty) -> None:
        """Set AI difficulty level"""
        self.difficulty = difficulty.value
    
    def set_win_points(self, points: int) -> None:
        """Set points needed to win"""
        self.win_points = max(1, min(50, points))
