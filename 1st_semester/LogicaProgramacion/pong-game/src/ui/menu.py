"""
Menu UI Component
"""

import pygame
from src import config
from src.ui.button import Button, InputBox


class Menu:
    """
    Main menu screen with START button and settings

    Features:
    - Game title display
    - START button to begin game
    - Input field for max win points
    - Instructions display
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize menu components

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Initialize fonts
        self.font_title = pygame.font.Font(None, config.FONT_LARGE + 30)
        self.font_subtitle = pygame.font.Font(None, config.FONT_MEDIUM)
        self.font_instructions = pygame.font.Font(None, config.FONT_SMALL)

        # Center positions
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Create START button (large and prominent)
        self.start_button = Button(
            x=center_x,
            y=center_y + 50,
            width=250,
            height=70,
            text="START",
            font_size=config.FONT_MEDIUM + 10,
            color=config.COLOR_CYAN,
            hover_color=config.COLOR_WHITE,
            text_color=config.COLOR_BLACK,
        )

        # Create QUIT button (red)
        self.quit_button = Button(
            x=center_x,
            y=center_y + 140,
            width=250,
            height=60,
            text="QUIT",
            font_size=config.FONT_MEDIUM,
            color=config.COLOR_RED,
            hover_color=config.COLOR_DARK_RED,
            text_color=config.COLOR_WHITE,
        )

        # Create win points input box
        self.win_points_input = InputBox(
            x=center_x,
            y=center_y - 50,
            width=100,
            height=50,
            initial_value=config.DEFAULT_WIN_POINTS,
            min_value=config.MIN_WIN_POINTS,
            max_value=config.MAX_WIN_POINTS,
            label="Points to Win",
        )

        # Track if start was requested
        self.start_requested = False

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame events for input box

        Args:
            event: Pygame event
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

        # Update input box with keyboard events
        self.win_points_input.update(mouse_pos, mouse_clicked, event)

    def update(self, mouse_pos: tuple, mouse_clicked: bool) -> tuple:
        """
        Update menu state

        Args:
            mouse_pos: Current mouse position
            mouse_clicked: Whether mouse was clicked this frame

        Returns:
            tuple: (start_clicked, quit_clicked)
        """
        start_clicked = False
        quit_clicked = False

        # Update start button
        if self.start_button.update(mouse_pos, mouse_clicked):
            self.start_requested = True
            start_clicked = True

        # Update quit button
        if self.quit_button.update(mouse_pos, mouse_clicked):
            quit_clicked = True

        # Update input box (for hover/click state)
        self.win_points_input.update(mouse_pos, mouse_clicked)

        return (start_clicked, quit_clicked)

    def get_win_points(self) -> int:
        """
        Get the configured win points

        Returns:
            int: Number of points needed to win
        """
        return self.win_points_input.get_value()

    def reset(self) -> None:
        """Reset menu state"""
        self.start_requested = False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Render menu to screen

        Args:
            screen: Pygame surface to draw on
        """
        center_x = self.screen_width // 2

        # Draw title "PONG"
        title = self.font_title.render("PONG", True, config.COLOR_CYAN)
        title_rect = title.get_rect(center=(center_x, 120))
        screen.blit(title, title_rect)

        # Draw subtitle
        subtitle = self.font_subtitle.render(
            "Classic Arcade Game", True, config.COLOR_WHITE
        )
        subtitle_rect = subtitle.get_rect(center=(center_x, 180))
        screen.blit(subtitle, subtitle_rect)

        # Draw win points input
        self.win_points_input.draw(screen)

        # Draw START button
        self.start_button.draw(screen)

        # Draw QUIT button
        self.quit_button.draw(screen)

        # Draw instructions at bottom
        instructions = [
            "Controls:",
            "W / S  -  Move paddle up/down",
            "SPACE  -  Pause game",
            "ESC    -  Return to menu",
        ]

        y_offset = self.screen_height - 150
        for line in instructions:
            text = self.font_instructions.render(line, True, config.COLOR_GRAY)
            text_rect = text.get_rect(center=(center_x, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30


class PauseMenu:
    """
    Pause menu overlay

    Features:
    - Resume button
    - Quit to main menu button
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize pause menu

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        center_x = screen_width // 2
        center_y = screen_height // 2

        self.font_title = pygame.font.Font(None, config.FONT_LARGE)

        # Create buttons
        self.resume_button = Button(
            x=center_x,
            y=center_y,
            width=200,
            height=60,
            text="RESUME",
            color=config.COLOR_CYAN,
            hover_color=config.COLOR_WHITE,
        )

        self.quit_button = Button(
            x=center_x,
            y=center_y + 80,
            width=200,
            height=60,
            text="QUIT",
            color=config.COLOR_GRAY,
            hover_color=config.COLOR_WHITE,
        )

        self.resume_requested = False
        self.quit_requested = False

    def update(self, mouse_pos: tuple, mouse_clicked: bool) -> tuple:
        """
        Update pause menu

        Args:
            mouse_pos: Current mouse position
            mouse_clicked: Whether mouse was clicked

        Returns:
            tuple: (resume_clicked, quit_clicked)
        """
        resume = self.resume_button.update(mouse_pos, mouse_clicked)
        quit_game = self.quit_button.update(mouse_pos, mouse_clicked)

        return (resume, quit_game)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Render pause menu overlay

        Args:
            screen: Pygame surface to draw on
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill(config.COLOR_BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))

        # Draw title
        title = self.font_title.render("PAUSED", True, config.COLOR_CYAN)
        title_rect = title.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 100)
        )
        screen.blit(title, title_rect)

        # Draw buttons
        self.resume_button.draw(screen)
        self.quit_button.draw(screen)


class GameOverMenu:
    """
    Game over screen with play again option
    """

    def __init__(self, screen_width: int, screen_height: int):
        """Initialize game over menu"""
        self.screen_width = screen_width
        self.screen_height = screen_height

        center_x = screen_width // 2
        center_y = screen_height // 2

        self.font_title = pygame.font.Font(None, config.FONT_LARGE + 20)
        self.font_score = pygame.font.Font(None, config.FONT_LARGE)

        # Create buttons
        self.play_again_button = Button(
            x=center_x,
            y=center_y + 80,
            width=250,
            height=60,
            text="PLAY AGAIN",
            color=config.COLOR_CYAN,
            hover_color=config.COLOR_WHITE,
        )

        self.menu_button = Button(
            x=center_x,
            y=center_y + 160,
            width=250,
            height=60,
            text="MAIN MENU",
            color=config.COLOR_GRAY,
            hover_color=config.COLOR_WHITE,
        )

        self.winner_text = ""
        self.player_score = 0
        self.cpu_score = 0

    def set_result(self, player_score: int, cpu_score: int, player_won: bool) -> None:
        """
        Set game result for display

        Args:
            player_score: Player's final score
            cpu_score: CPU's final score
            player_won: True if player won
        """
        self.player_score = player_score
        self.cpu_score = cpu_score
        self.winner_text = "YOU WIN!" if player_won else "GAME OVER"

    def update(self, mouse_pos: tuple, mouse_clicked: bool) -> tuple:
        """
        Update game over menu

        Returns:
            tuple: (play_again_clicked, menu_clicked)
        """
        play_again = self.play_again_button.update(mouse_pos, mouse_clicked)
        menu = self.menu_button.update(mouse_pos, mouse_clicked)

        return (play_again, menu)

    def draw(self, screen: pygame.Surface) -> None:
        """Render game over screen"""
        center_x = self.screen_width // 2

        # Draw winner text
        color = config.COLOR_CYAN if "WIN" in self.winner_text else config.COLOR_WHITE
        title = self.font_title.render(self.winner_text, True, color)
        title_rect = title.get_rect(center=(center_x, self.screen_height // 2 - 100))
        screen.blit(title, title_rect)

        # Draw final score
        score_text = f"{self.player_score} - {self.cpu_score}"
        score = self.font_score.render(score_text, True, config.COLOR_WHITE)
        score_rect = score.get_rect(center=(center_x, self.screen_height // 2 - 20))
        screen.blit(score, score_rect)

        # Draw buttons
        self.play_again_button.draw(screen)
        self.menu_button.draw(screen)
