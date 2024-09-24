# modules/dark_side.py

import pygame
import logging
from modules.settings import WIDTH, HEIGHT, COLORS

def dark_side_choice(screen):
    """
    Presents a Dark Side choice to the player.

    Args:
        screen (pygame.Surface): The Pygame screen surface.

    Returns:
        bool: True if the player chooses to increase obstacle speed, False otherwise.
    """
    font = pygame.font.Font(None, 40)
    prompt = "Choose Dark Side: Press 'D' to increase obstacle speed or any other key for shield."
    text_surface = font.render(prompt, True, COLORS['RED'])
    screen.blit(text_surface, (WIDTH // 6, HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    logging.info("Player chose Dark Side: Increased obstacle speed.")
                    return True
                else:
                    logging.info("Player chose to activate Shield instead of Dark Side.")
                    return False
