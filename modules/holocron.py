# modules/holocron.py

import pygame
import random
from modules.settings import HOLOCRON_SIZE, HOLOCRON_COLOR, PIPE_SPEED
import logging

class Holocron:
    def __init__(self, screen_width, screen_height):
        self.size = HOLOCRON_SIZE
        self.color = HOLOCRON_COLOR
        self.rect = pygame.Rect(
            screen_width,
            random.randint(0, screen_height - self.size),
            self.size,
            self.size
        )
        self.speed = PIPE_SPEED  # Same speed as pipes

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def collect(self, bird_rect):
        """Check if bird has collected the holocron."""
        if self.rect.colliderect(bird_rect):
            return True
        return False
