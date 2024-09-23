# modules/holocron.py

import pygame
from modules.settings import HOLOCRON_SIZE, HOLOCRON_COLOR  # Ensure these are defined in settings
import random

class Holocron:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.Surface((HOLOCRON_SIZE, HOLOCRON_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, HOLOCRON_COLOR, (HOLOCRON_SIZE//2, HOLOCRON_SIZE//2), HOLOCRON_SIZE//2)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width + 200
        self.rect.y = random.randint(0, screen_height - HOLOCRON_SIZE)
        self.speed = 5  # Adjust as needed
    
    def update(self):
        """Moves the holocron to the left based on its speed."""
        self.rect.x -= self.speed
    
    def draw(self, screen):
        """Draws the holocron on the screen."""
        screen.blit(self.image, self.rect)
    
    def collect(self, bird_rect):
        """Checks if the bird has collected the holocron."""
        return self.rect.colliderect(bird_rect)
    
    def off_screen(self):
        """Checks if the holocron has moved off the screen."""
        return self.rect.right < 0
