"""
UI Manager - Central coordinator for all UI components
"""

import pygame
from src.ui.menu import Menu, PauseMenu, GameOverMenu
from src.utils.constants import GameState


class UIManager:
    """
    Manages all UI components and their interactions

    Features:
    - Centralizes UI component management
    - Handles state-specific UI rendering
    - Coordinates UI input handling
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize UI manager with all menus

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Initialize all menu components
        self.main_menu = Menu(screen_width, screen_height)
        self.pause_menu = PauseMenu(screen_width, screen_height)
        self.game_over_menu = GameOverMenu(screen_width, screen_height)

        # Track mouse click state (set by events)
        self.mouse_just_clicked = False
        self.mouse_pos = (0, 0)

    def handle_event(self, event: pygame.event.Event, current_state: GameState) -> dict:
        """
        Handle pygame events for UI components

        Args:
            event: Pygame event
            current_state: Current game state

        Returns:
            dict: Actions to perform based on UI interaction
        """
        actions = {
            "start_game": False,
            "resume_game": False,
            "quit_to_menu": False,
            "play_again": False,
            "win_points": None,
        }

        # Track mouse click on MOUSEBUTTONDOWN event (left click)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_just_clicked = True

        self.mouse_pos = pygame.mouse.get_pos()

        # Handle state-specific events
        if current_state == GameState.MENU:
            self.main_menu.handle_event(event)

        return actions

    def update(self, current_state: GameState) -> dict:
        """
        Update UI based on current game state

        Args:
            current_state: Current game state

        Returns:
            dict: Actions triggered by UI
        """
        actions = {
            "start_game": False,
            "resume_game": False,
            "quit_to_menu": False,
            "play_again": False,
            "quit_game": False,
            "win_points": None,
        }

        self.mouse_pos = pygame.mouse.get_pos()

        # Use the click state set by handle_event
        mouse_clicked = self.mouse_just_clicked

        if current_state == GameState.MENU:
            start_clicked, quit_clicked = self.main_menu.update(
                self.mouse_pos, mouse_clicked
            )
            if start_clicked:
                actions["start_game"] = True
                actions["win_points"] = self.main_menu.get_win_points()
            if quit_clicked:
                actions["quit_game"] = True

        elif current_state == GameState.PAUSED:
            resume, quit_game = self.pause_menu.update(self.mouse_pos, mouse_clicked)
            actions["resume_game"] = resume
            actions["quit_to_menu"] = quit_game

        elif current_state == GameState.GAME_OVER:
            play_again, menu = self.game_over_menu.update(self.mouse_pos, mouse_clicked)
            actions["play_again"] = play_again
            actions["quit_to_menu"] = menu

        # Reset the click flag after processing
        self.mouse_just_clicked = False

        return actions

    def set_game_over_result(
        self, player_score: int, cpu_score: int, player_won: bool
    ) -> None:
        """
        Set game over screen result

        Args:
            player_score: Player's final score
            cpu_score: CPU's final score
            player_won: True if player won
        """
        self.game_over_menu.set_result(player_score, cpu_score, player_won)

    def reset_menu(self) -> None:
        """Reset main menu state"""
        self.main_menu.reset()

    def draw(self, screen: pygame.Surface, current_state: GameState) -> None:
        """
        Draw UI based on current game state

        Args:
            screen: Pygame surface to draw on
            current_state: Current game state
        """
        if current_state == GameState.MENU:
            self.main_menu.draw(screen)

        elif current_state == GameState.PAUSED:
            self.pause_menu.draw(screen)

        elif current_state == GameState.GAME_OVER:
            self.game_over_menu.draw(screen)
