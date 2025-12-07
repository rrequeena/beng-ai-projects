"""
Collision Detection and Response System
SOLID: Single Responsibility - Collision handling only
"""
import pygame
from typing import Tuple, Optional
from src.entities.ball import Ball
from src.entities.paddle import Paddle
from src import config

class CollisionSystem:
    """
    Detects collisions and triggers responses
    
    Responsibilities:
    - Detect collisions between objects
    - Trigger appropriate collision responses
    - NOT responsible for physics (see PhysicsSystem)
    
    Algorithm: AABB (Axis-Aligned Bounding Box) collision detection - O(1)
    """
    
    @staticmethod
    def check_paddle_collision(ball: Ball, paddle: Paddle) -> bool:
        """
        Check if ball collides with paddle
        
        Algorithm:
        1. Get bounding rectangles for both objects
        2. Use pygame AABB collision detection (rectangular overlap)
        3. Return collision result
        
        Complexity: O(1)
        
        Args:
            ball: Ball object
            paddle: Paddle object
            
        Returns:
            bool: True if collision detected
        """
        return ball.get_rect().colliderect(paddle.get_rect())
    
    @staticmethod
    def handle_paddle_collision(ball: Ball, paddle: Paddle) -> None:
        """
        Handle ball-paddle collision response
        
        Args:
            ball: Ball that collided
            paddle: Paddle that was hit
        """
        is_left = paddle.is_left
        ball.handle_paddle_collision(paddle.get_rect(), is_left)
    
    @staticmethod
    def check_multiple_paddles(ball: Ball, paddles: list) -> Optional[Paddle]:
        """
        Check collision with multiple paddles
        
        Args:
            ball: Ball object
            paddles: List of paddle objects
            
        Returns:
            Paddle that was hit, or None if no collision
        """
        for paddle in paddles:
            if CollisionSystem.check_paddle_collision(ball, paddle):
                return paddle
        return None
