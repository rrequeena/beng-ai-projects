"""
Ball Entity - Physics and behavior of the pong ball
"""

import pygame
from src.entities.entity import Entity
from src import config


class Ball(Entity):
    """
    Represents the game ball with physics simulation

    Physics Model:
    - Moves in straight line with constant velocity
    - Bounces off top/bottom walls (velocity Y inverted)
    - Bounces off paddles (velocity X inverted + speed increase)
    - Leaves play area = point scored
    """

    def __init__(self, x: float, y: float):
        """Initialize ball at center with default velocity"""
        super().__init__(x, y, config.BALL_SIZE, config.BALL_SIZE)
        self.velocity_x = -config.BALL_INITIAL_SPEED  # Start toward left
        self.velocity_y = 0
        self.initial_x = x
        self.initial_y = y

    def update(self, dt: float, screen_height: int) -> bool:
        """
        Update ball position with physics

        Args:
            dt: Delta time (seconds)
            screen_height: Screen height for boundary checking

        Returns:
            bool: True if ball is out of bounds (goal scored)
        """
        # Update position based on velocity (integration)
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        # Bounce off top and bottom walls
        if self.y <= 0 or self.y + self.height >= screen_height:
            self.velocity_y = -self.velocity_y
            # Keep ball in bounds
            self.y = max(0, min(self.y, screen_height - self.height))

        # Check if ball left play area (out of bounds)
        if self.x < 0 or self.x > config.SCREEN_WIDTH:
            return True  # Ball is out of bounds

        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw ball as filled circle"""
        center = (int(self.x + self.width / 2), int(self.y + self.height / 2))
        pygame.draw.circle(surface, config.COLOR_WHITE, center, self.width // 2)

    def handle_paddle_collision(
        self, paddle_rect: pygame.Rect, is_left_paddle: bool
    ) -> None:
        """
        Handle collision with paddle - includes speed calculation algorithm

        Algorithm:
        1. Invert horizontal velocity (bounce)
        2. Calculate hit location on paddle (0 = top, 1 = bottom)
        3. Add angular velocity based on hit location
        4. Increase speed by 5% (up to max)

        Args:
            paddle_rect: Rectangle of paddle that was hit
            is_left_paddle: True if left paddle, False if right
        """
        # Invert horizontal velocity (bounce)
        self.velocity_x = -self.velocity_x * config.SPEED_INCREMENT

        # Cap maximum speed
        if abs(self.velocity_x) > config.BALL_MAX_SPEED:
            self.velocity_x = (
                config.BALL_MAX_SPEED if self.velocity_x > 0 else -config.BALL_MAX_SPEED
            )

        # Calculate hit location on paddle (normalized 0.0 to 1.0)
        # 0.5 = center (no spin), 0.0 = top (negative spin), 1.0 = bottom (positive spin)
        ball_center_y = self.y + self.height / 2
        paddle_center_y = paddle_rect.centery
        hit_offset = (ball_center_y - paddle_center_y) / (paddle_rect.height / 2)
        hit_offset = max(-1.0, min(1.0, hit_offset))  # Clamp to [-1, 1]

        # Add angular velocity (spin) - max 300 pixels/sec vertical
        angular_velocity = hit_offset * 300
        self.velocity_y = angular_velocity

        # Move ball slightly out of paddle to prevent re-collision
        offset = config.PADDLE_WIDTH + 5
        if is_left_paddle:
            self.x = paddle_rect.right + offset
        else:
            self.x = paddle_rect.left - offset

    def reset(self) -> None:
        """Reset ball to center with initial speed"""
        self.x = self.initial_x
        self.y = self.initial_y
        self.velocity_x = -config.BALL_INITIAL_SPEED
        self.velocity_y = 0
