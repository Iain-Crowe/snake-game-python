from __future__ import annotations

from abc import ABC

import pygame


class Component(ABC):
    """Base class for all components."""

    def __init__(self, entity_id: int) -> None:
        self.entity_id = entity_id


class Position(Component):
    """Component that represents a position in the grid."""

    def __init__(self, entity_id: int, x: int, y: int) -> None:
        """Initialize the position.
        @param entity_id: The entity ID.
        @param x: The x-coordinate.
        @param y: The y-coordinate.
        """
        super().__init__(entity_id)
        self.x = x
        self.y = y

    def __sub__(self, other: Position) -> Direction:
        dx = self.x - other.x
        dy = self.y - other.y

        if abs(dx) > 1 or abs(dy) > 1:
            raise ValueError("Positions are not adjacent; cannot determine direction.")

        return Direction(self.entity_id, (dx, dy))

    def __eq__(self, other: Position) -> bool:
        return self.x == other.x and self.y == other.y


class Direction(Component):
    """Component that represents a direction."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self, entity_id: int, direction: tuple[int, int]) -> None:
        """Initialize the direction.
        @param entity_id: The entity ID.
        @param direction: The direction as a tuple of (dx, dy)."""
        super().__init__(entity_id)
        self.value = direction

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

    def opposes(self, other: Direction) -> bool:
        """Check if the direction opposes another direction.
        @param other: The other direction.
        @return: True if the directions oppose each other, False otherwise."""
        return self.dx == -other.dx and self.dy == -other.dy


class Collider(Component):
    """Component that represents a collider."""

    def __init__(self, entity_id: int, x: int, y: int) -> None:
        """Initialize the collider."""
        super().__init__(entity_id)

        self.pos = Position(entity_id, x, y)

    def collides_with(self, other: Collider) -> bool:
        """Check if this collider collides with another collider.
        @param other: The other collider.
        @return: True if the colliders collide, False otherwise."""
        return self.pos == other.pos


class Input(Component):
    """Component that represents input from the user."""

    def __init__(self, entity_id):
        """Initialize the input component."""
        super().__init__(entity_id)

        self.last_input = Direction.UP

    @property
    def last(self) -> Direction:
        """Get the last input direction.
        @return: The last input direction."""
        return Direction(self.entity_id, self.last_input)

    def get_input(self) -> Direction:
        """Get input from the user.
        @return: The input direction."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not self.last.opposes(
            Direction(self.entity_id, Direction.UP)
        ):
            self.last_input = Direction.UP
            return Direction(self.entity_id, Direction.UP)  # UP
        elif keys[pygame.K_DOWN] and not self.last.opposes(
            Direction(self.entity_id, Direction.DOWN)
        ):
            self.last_input = Direction.DOWN
            return Direction(self.entity_id, Direction.DOWN)  # DOWN
        elif keys[pygame.K_LEFT] and not self.last.opposes(
            Direction(self.entity_id, Direction.LEFT)
        ):
            self.last_input = Direction.LEFT
            return Direction(self.entity_id, Direction.LEFT)  # LEFT
        elif keys[pygame.K_RIGHT] and not self.last.opposes(
            Direction(self.entity_id, Direction.RIGHT)
        ):
            self.last_input = Direction.RIGHT
            return Direction(self.entity_id, Direction.RIGHT)  # RIGHT
        else:
            return self.last
