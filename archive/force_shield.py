# modules/force_shield.py

import pygame
import time
from modules.settings import BLUE, FPS
import logging

def activate_force_shield(bird, screen, duration=3):
    """
    Activates a shield around the bird for a specified duration.

    Args:
        bird (Bird): The bird object to protect.
        screen (pygame.Surface): The Pygame screen surface.
        duration (int, optional): Duration of the shield in seconds. Defaults to 3.
    """
    bird.shield_active = True
    bird.shield_duration = duration * FPS  # Convert seconds to frames
    logging.info("Force shield activated.")

    # Optional: Add visual effects or sounds here
    # For example, play a shield sound
    # pygame.mixer.Sound('assets/shield.wav').play()

    # Visual effect: Draw a shield immediately
    # Note: The actual drawing should be handled in the Bird's draw method
