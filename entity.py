from abc import ABC, abstractmethod
from typing import List
from component import Direction, Position, Input, Collider
import pygame
from const import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
import random


class Entity(ABC):
    """Class that represents an entity."""

    def __init__(self, id: int) -> None:
        self.id = id

    @abstractmethod
    def update(self) -> None:
        """Update the entity."""
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Render the entity.
        @param screen: The screen to render the entity on."""
        pass


class EntityManager:
    """Class that manages entities."""

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock) -> None:
        """Initialize the entity manager."""
        self.entities: List[Entity] = [
            Apple(
                1,
                x=random.randint(0, GRID_WIDTH - 1),
                y=random.randint(0, GRID_HEIGHT - 1),
            ),
            Snake(
                0,
                x=random.randint(GRID_WIDTH // 4, 3 * GRID_WIDTH // 4),
                y=random.randint(GRID_HEIGHT // 4, 3 * GRID_HEIGHT // 4),
            ),
        ]
        self.score_bar = ScoreBar(2)

        self.screen = screen
        self.clock = clock

        self.game_over = False

    @property
    def snake_lenth(self) -> int:
        """Get the length of the snake."""
        return len(self.entities[1].segments)

    def update(self) -> None:
        # Check if the snake filled the grid
        if self.snake_lenth == GRID_WIDTH * GRID_HEIGHT:
            print("Game Over! Snake filled the grid.")
            self.game_over = True

        # Check if the game is over
        if self.game_over:
            return

        # Update the score bar
        self.score_bar.score = self.snake_lenth

        # Update the entities
        for entity in self.entities:
            entity.update()

        self.check_collisions()

    def render(self) -> None:
        # Render the game over screen if game is over
        if self.game_over:
            self.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, GRID_WIDTH)
            text = font.render("Game Over!", True, (255, 0, 0))
            text_rect = text.get_rect(
                center=(GRID_WIDTH * GRID_SIZE / 2, GRID_HEIGHT * GRID_SIZE / 2)
            )
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            return

        # Render the entities
        self.screen.fill((0, 0, 0))
        self.score_bar.render(self.screen)
        for entity in self.entities:
            entity.render(self.screen)
        pygame.display.flip()

    def check_collisions(self) -> None:
        # Reference to the snake and apple
        snake: Snake = self.entities[1]
        apple: Apple = self.entities[0]

        # Check if the snake collided with the walls
        head = snake.segments[0]
        if (
            head.pos.x < 0
            or head.pos.x >= GRID_WIDTH
            or head.pos.y < 0
            or head.pos.y >= GRID_HEIGHT - 1
        ):
            print("Game Over! Snake collided with walls.")
            self.game_over = True

        # Check other collisions
        if snake.check_collision(apple):
            print("Game Over! Snake collided with itself.")
            self.game_over = True


class Segment(Entity):
    """Class that represents a segment of the snake."""

    def __init__(
        self, id: int, x: int = 0, y: int = 0, direction: Direction = Direction.UP
    ) -> None:
        """Initialize the segment.
        @param id: The entity ID.
        @param x: The x-coordinate of the segment.
        @param y: The y-coordinate of the segment.
        @param direction: The direction of the segment."""
        super().__init__(id)

        self.pos = Position(id, x=x, y=y)
        self.direction = Direction(id, direction=direction)

        self.collider = Collider(id, x, y)

    def update(self) -> None:
        self.pos.x += self.direction.dx
        self.pos.y += self.direction.dy
        self.collider.pos = self.pos

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(
            (0, 255, 0),
            (self.pos.x * GRID_SIZE, self.pos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )


class Snake(Entity):
    """Class that represents the snake entity."""

    def __init__(self, id: int, x: int = 0, y: int = 0) -> None:
        """Initialize the snake.
        @param id: The entity ID.
        @param x: The x-coordinate of the snake.
        @param y: The y-coordinate of the snake."""
        super().__init__(id)

        self.segments: List[Segment] = [Segment(i, x, y + i) for i in range(3)]
        self.input = Input(id)

    def update(self) -> None:
        prev_directions = [segment.direction for segment in self.segments]

        head_input = self.input.get_input()
        self.segments[0].direction = head_input
        self.segments[0].update()

        for i in range(1, len(self.segments)):
            self.segments[i].direction = prev_directions[i - 1]
            self.segments[i].update()

    def render(self, screen: pygame.Surface) -> None:
        for segment in self.segments:
            segment.render(screen)

    def check_collision(self, apple: "Apple") -> bool:
        """Check if the snake collided with itself or the apple.
        @param apple: The apple entity.
        @return: True if the snake collided with itself or the apple, False otherwise.
        """
        # Reference to the head of the snake
        head = self.segments[0]

        # Check if the snake collided with itself
        for segment in self.segments[1:]:
            if head.collider.collides_with(segment.collider):
                return True

        # Check if the snake collided with the apple and grow if it did
        if head.collider.collides_with(apple.collider):
            self.grow()
            apple.respawn()
            print("Apple eaten!")

        return False

    def grow(self) -> None:
        """Grow the snake by adding a new segment."""
        tail = self.segments[-1]
        self.segments.append(
            Segment(
                len(self.segments),
                x=tail.pos.x - tail.direction.dx,
                y=tail.pos.y - tail.direction.dy,
                direction=tail.direction,
            )
        )


class Apple(Entity):
    """Class that represents the apple entity."""

    def __init__(self, id: int, x: int = 0, y: int = 0) -> None:
        """Initialize the apple.
        @param id: The entity ID.
        @param x: The x-coordinate of the apple.
        @param y: The y-coordinate of the apple."""
        super().__init__(id)

        self.pos = Position(id, x=x, y=y)
        self.collider = Collider(id, x, y)

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(
            (255, 0, 0),
            (self.pos.x * GRID_SIZE, self.pos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )

    def respawn(self) -> None:
        """Respawn the apple at a random location."""
        self.pos.x = random.randint(0, GRID_WIDTH - 1)
        self.pos.y = random.randint(0, GRID_HEIGHT - 2)
        self.collider.pos = self.pos


class ScoreBar(Entity):
    """Class that represents the score bar entity."""

    def __init__(self, id):
        """Initialize the score bar."""
        super().__init__(id)
        self.score = 0
        self.font = pygame.font.Font(None, GRID_SIZE)

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        screen.fill(
            (255, 255, 255),
            (0, GRID_HEIGHT * GRID_SIZE - GRID_SIZE, GRID_WIDTH * GRID_SIZE, GRID_SIZE),
        )
        text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(text, (4, GRID_HEIGHT * GRID_SIZE - 17))
