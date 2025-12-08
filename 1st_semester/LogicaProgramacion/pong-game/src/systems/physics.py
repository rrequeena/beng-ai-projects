"""
Physics System - All movement calculations
"""

from typing import List
from src.entities.entity import Entity
from src.entities.ball import Ball


class PhysicsSystem:
    """
    Manages all physics calculations for game entities

    Responsibilities:
    - Update entity positions based on velocity
    - Handle world boundaries (ball bounce off walls)
    - NOT responsible for collision response (see CollisionSystem)
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize physics system

        Args:
            screen_width: Game screen width
            screen_height: Game screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, entities: List[Entity], dt: float) -> bool:
        """
        Update all entities physics

        Algorithm:
        1. For each entity, call its update method
        2. For ball specifically, check boundary conditions
        3. Return if goal was scored

        Args:
            entities: List of entities to update
            dt: Delta time (seconds)

        Returns:
            bool: True if a goal was scored (ball out of bounds)
        """
        goal_scored = False

        for entity in entities:
            if isinstance(entity, Ball):
                # Ball has special boundary logic
                goal_scored = entity.update(dt, self.screen_height)
            else:
                # Paddles and other entities
                entity.update(dt)

        return goal_scored

    def apply_force(self, entity: Entity, force_x: float, force_y: float) -> None:
        """
        Apply instantaneous force to entity (for future expansion)

        Args:
            entity: Entity to apply force to
            force_x: Force in X direction
            force_y: Force in Y direction
        """
        entity.velocity_x += force_x
        entity.velocity_y += force_y
