"""
AI System - CPU Player Decision Making
SOLID: Single Responsibility - AI logic only
Strategy Pattern: Different difficulty levels use different algorithms
"""

import random
from src.entities.paddle import Paddle
from src.entities.ball import Ball
from src import config


class AISystem:
    """
    Controls CPU paddle movement with difficulty levels

    The AI is intentionally imperfect to make the game fun and winnable.
    It makes random movements and only occasionally reacts to the ball.
    """

    def __init__(self, difficulty_level: float = config.AIDifficulty.MEDIUM):
        """
        Initialize AI with difficulty level

        Args:
            difficulty_level: Speed multiplier (0.0 to 1.0)
        """
        self.difficulty = difficulty_level
        self.reaction_timer = 0.0
        self.random_move_timer = 0.0
        self.current_action = "idle"  # "idle", "up", "down", "track"

        # Set parameters based on difficulty
        self._configure_difficulty()

    def _configure_difficulty(self) -> None:
        """Configure AI parameters based on difficulty level"""
        if self.difficulty <= config.AIDifficulty.EASY:
            self.track_chance = 0.2  # 20% chance to actually track the ball
            self.reaction_delay = 0.7  # Very slow reactions
            self.random_move_duration = 1.0  # How long random moves last
        elif self.difficulty <= config.AIDifficulty.MEDIUM:
            self.track_chance = 0.35  # 35% chance to track the ball
            self.reaction_delay = 0.5  # Moderate reactions
            self.random_move_duration = 0.7
        else:
            self.track_chance = 0.55  # 55% chance to track the ball
            self.reaction_delay = 0.3  # Faster reactions
            self.random_move_duration = 0.4

    def update(self, paddle: Paddle, ball: Ball, dt: float) -> None:
        """
        Update CPU paddle position - mostly random with occasional ball tracking
        """
        self.reaction_timer -= dt
        self.random_move_timer -= dt

        # Time to make a new decision?
        if self.reaction_timer <= 0:
            self.reaction_timer = self.reaction_delay
            self._make_decision(paddle, ball)

        # Execute current action
        if self.random_move_timer <= 0:
            # Random move expired, maybe change direction
            if random.random() < 0.3:  # 30% chance to change
                self.current_action = random.choice(
                    ["idle", "up", "down", "idle", "idle"]
                )
                self.random_move_timer = self.random_move_duration

        self._execute_action(paddle, ball)

    def _make_decision(self, paddle: Paddle, ball: Ball) -> None:
        """Decide what to do - track ball or move randomly"""

        # Only consider tracking if ball is coming toward AI
        if ball.velocity_x > 0:
            # Ball coming toward AI - maybe track it
            if random.random() < self.track_chance:
                self.current_action = "track"
            else:
                # Random movement instead
                self.current_action = random.choice(["up", "down", "idle"])
                self.random_move_timer = self.random_move_duration
        else:
            # Ball going away - do random stuff or idle
            self.current_action = random.choice(["up", "down", "idle", "idle", "idle"])
            self.random_move_timer = self.random_move_duration

    def _execute_action(self, paddle: Paddle, ball: Ball) -> None:
        """Execute the current action"""
        if self.current_action == "track":
            self._track_ball(paddle, ball)
        elif self.current_action == "up":
            paddle.move_up()
        elif self.current_action == "down":
            paddle.move_down()
        else:  # idle
            paddle.stop()

    def _track_ball(self, paddle: Paddle, ball: Ball) -> None:
        """Actually try to track the ball (but imperfectly)"""
        paddle_center = paddle.y + paddle.height / 2
        ball_center = ball.y + ball.height / 2

        # Add significant error to make it beatable
        error = random.randint(-70, 70)
        target = ball_center + error

        # Large dead zone - AI is lazy
        dead_zone = 60

        if target < paddle_center - dead_zone:
            paddle.move_up()
        elif target > paddle_center + dead_zone:
            paddle.move_down()
        else:
            # Close enough, mostly stop
            if random.random() < 0.7:
                paddle.stop()
            else:
                # Sometimes move wrong direction
                if random.random() < 0.5:
                    paddle.move_up()
                else:
                    paddle.move_down()

    def set_difficulty(self, difficulty_level: float) -> None:
        """Change AI difficulty at runtime"""
        self.difficulty = difficulty_level
        self._configure_difficulty()
