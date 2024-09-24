# modules/force_lightning.py

import pygame
from modules.settings import COLORS, FPS  # Import the COLORS dictionary and FPS
import logging

def activate_force_lightning(bird, obstacles, screen, duration=3):
    """
    Activates a lightning effect around the bird, destroying obstacles upon collision.

    Args:
        bird (Bird): The bird object to affect.
        obstacles (list): List of current obstacle objects.
        screen (pygame.Surface): The Pygame screen surface.
        duration (int, optional): Duration of the lightning effect in seconds. Defaults to 3.
    """
    bird.lightsaber_active = True
    logging.info("Lightning activated.")

    lightning_duration = duration * FPS  # Convert seconds to frames
    white_color = COLORS['WHITE']  # Retrieve the WHITE color from the COLORS dictionary

    while lightning_duration > 0:
        for obstacle in obstacles:
            if obstacle.top_rect.colliderect(bird.rect) or obstacle.bottom_rect.colliderect(bird.rect):
                obstacle.top_rect.height = 0
                obstacle.bottom_rect.height = 0
                # Draw lightning lines
                pygame.draw.line(screen, white_color, bird.rect.center, obstacle.top_rect.midbottom, 2)
                pygame.draw.line(screen, white_color, bird.rect.center, obstacle.bottom_rect.midtop, 2)
        pygame.display.flip()
        lightning_duration -= 1
        pygame.time.delay(int(1000 / FPS))  # Delay to match FPS

    bird.lightsaber_active = False
    logging.info("Lightning deactivated.")
