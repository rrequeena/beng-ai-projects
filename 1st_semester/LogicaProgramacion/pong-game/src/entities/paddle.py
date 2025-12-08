"""
Paddle Entity - Player and CPU paddles
"""

import pygame
from src.entities.entity import Entity
from src import config


class Paddle(Entity):
    """
    Represents a game paddle (player or CPU)

    Responsibility:
    - Update position based on velocity
    - Clamp position to screen bounds
    - Render paddle rectangle
    """

    def __init__(self, x: float, y: float, is_left: bool = True):
        """
        Initialize paddle

        Args:
            x: X position (pixels)
            y: Y position (pixels)
            is_left: True for left paddle, False for right
        """
        super().__init__(x, y, config.PADDLE_WIDTH, config.PADDLE_HEIGHT)
        self.is_left = is_left
        self.min_y = 0
        self.max_y = config.SCREEN_HEIGHT - config.PADDLE_HEIGHT

    def update(self, dt: float) -> None:
        """
        Update paddle position based on velocity

        Args:
            dt: Delta time (seconds)
        """
        # Update position
        self.y += self.velocity_y * dt

        # Clamp to screen bounds
        self.y = max(self.min_y, min(self.y, self.max_y))

        # Stop velocity at end of movement (friction simulation)
        if self.y <= self.min_y or self.y >= self.max_y:
            self.velocity_y = 0

    def draw(self, surface: pygame.Surface) -> None:
        """Draw paddle as filled rectangle"""
        rect = self.get_rect()
        pygame.draw.rect(surface, config.COLOR_CYAN, rect)

    def move_up(self) -> None:
        """Set velocity to move upward"""
        self.velocity_y = -config.PADDLE_SPEED

    def move_down(self) -> None:
        """Set velocity to move downward"""
        self.velocity_y = config.PADDLE_SPEED

    def stop(self) -> None:
        """Stop paddle movement"""
        self.velocity_y = 0
