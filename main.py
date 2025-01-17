import pygame

from entity import EntityManager
from const import WINDOW_SIZE


def main() -> None:
    # Initialize the game
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    running = True
    playing = False

    # Initialize the entity manager
    entity_manager = EntityManager(screen, clock)

    # Main game loop
    while running:
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Await user input to start the game
        if not playing:
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, WINDOW_SIZE[0] // 20)
            text = font.render("Press any key to start", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    playing = True

            continue

        # Get input from the user continuously
        entity_manager.entities[1].input.get_input()

        # Update and render the entities
        entity_manager.update()
        entity_manager.render()
        clock.tick(12)

    pygame.quit()


if __name__ == "__main__":
    main()
