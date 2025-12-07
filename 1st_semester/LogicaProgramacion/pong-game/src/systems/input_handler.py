"""
Input Handling System
SOLID: Single Responsibility - Input processing only
"""
import pygame
from src.utils.constants import GameState

class InputHandler:
    """
    Processes player input and manages game state transitions
    
    Responsibilities:
    - Capture keyboard and mouse events
    - Update paddle movement
    - Request game state changes
    - NOT responsible for game logic
    """
    
    def __init__(self):
        """Initialize input handler"""
        self.keys_pressed = {}
        self.quit_requested = False
        self.pause_requested = False
        self.menu_requested = False
    
    def handle_events(self) -> None:
        """
        Process pygame events
        
        Events handled:
        - QUIT: Close window
        - KEYDOWN: Start movement or request state change
        - KEYUP: Stop movement
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
            
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed[event.key] = True
                
                # Handle special keys
                if event.key == pygame.K_SPACE:
                    self.pause_requested = True
                elif event.key == pygame.K_ESCAPE:
                    self.menu_requested = True
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed[event.key] = False
    
    def get_player_input(self) -> tuple:
        """
        Get current player movement input
        
        Returns:
            tuple: (move_up, move_down) boolean values
        """
        move_up = self.keys_pressed.get(pygame.K_w, False)
        move_down = self.keys_pressed.get(pygame.K_s, False)
        return (move_up, move_down)
    
    def reset_requests(self) -> None:
        """Reset action requests (after they're processed)"""
        self.pause_requested = False
        self.menu_requested = False
