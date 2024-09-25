# modules/jedi_training.py

import pygame
from modules.settings import WIDTH, HEIGHT, COLORS
import logging
import sys

def jedi_training(screen):
    """
    Prompts the player to press a specific key sequence (W, A, S, D) to pass Jedi training.

    Args:
        screen (pygame.Surface): The Pygame screen surface.

    Returns:
        bool: True if the player successfully completes the sequence, False otherwise.
    """
    font = pygame.font.Font(None, 50)
    prompt = "Jedi Training: Press W, A, S, D in sequence"
    text_surface = font.render(prompt, True, COLORS['GREEN'])
    screen.blit(text_surface, (WIDTH // 4, HEIGHT // 2 - 100))
    pygame.display.flip()

    sequence = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
    user_sequence = []

    while len(user_sequence) < len(sequence):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                user_sequence.append(event.key)
                if user_sequence != sequence[:len(user_sequence)]:
                    logging.info("Jedi training failed.")
                    return False  # Failure

    logging.info("Jedi training succeeded.")
    return True  # Success
