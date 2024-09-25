# modules/holocron.py

import pygame
import random
import logging
import os
from modules.settings import HOLOCRON_SETTINGS, COLORS

class Holocron:
    """
    Represents a Holocron in the game.
    """
    def __init__(self, screen_width, screen_height):
        self.size = HOLOCRON_SETTINGS['size']
        self.color = HOLOCRON_SETTINGS['color']
        self.rect = pygame.Rect(
            screen_width,
            random.randint(0, screen_height - self.size),
            self.size,
            self.size
        )
        self.speed = HOLOCRON_SETTINGS['speed']  # Using the speed from settings

    def update(self, dt):
        """
        Updates the Holocron's position.

        Args:
            dt (float): Delta time to scale movement speed.
        """
        self.rect.x -= self.speed * dt * 60  # Adjust movement based on delta time

    def draw(self, screen):
        """
        Draws the Holocron on the screen.

        Args:
            screen (pygame.Surface): The game screen to draw on.
        """
        pygame.draw.ellipse(screen, self.color, self.rect)

    def collect(self, bird_rect):
        """
        Checks if the bird has collected the holocron.

        Args:
            bird_rect (pygame.Rect): The bird's rectangle.

        Returns:
            bool: True if collected, False otherwise.
        """
        if self.rect.colliderect(bird_rect):
            logging.info("Holocron collected!")
            return True
        return False
