# modules/holocron.py

import pygame
import random
import logging
from modules.settings import HOLOCRON_SETTINGS

class Holocron:
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

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def collect(self, bird_rect):
        """Check if bird has collected the holocron."""
        return self.rect.colliderect(bird_rect)
