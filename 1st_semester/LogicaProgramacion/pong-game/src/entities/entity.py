"""
Base Entity Class - Abstract base for all game objects
"""

from abc import ABC, abstractmethod
import pygame


class Entity(ABC):
    """Abstract base class for all game entities"""

    def __init__(self, x: float, y: float, width: float, height: float):
        """
        Initialize entity with position and dimensions

        Args:
            x: X position (pixels)
            y: Y position (pixels)
            width: Entity width (pixels)
            height: Entity height (pixels)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0.0
        self.velocity_y = 0.0

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update entity state each frame

        Args:
            dt: Delta time since last frame (seconds)
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        Render entity to screen

        Args:
            surface: Pygame surface to draw on
        """
        pass

    def get_rect(self) -> pygame.Rect:
        """
        Get bounding rectangle for collision detection

        Returns:
            pygame.Rect: Rectangle representing entity bounds
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_center(self) -> tuple:
        """Get center point of entity"""
        return (self.x + self.width / 2, self.y + self.height / 2)
