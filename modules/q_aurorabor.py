# quantum_elements/AuroraBorealis.py

import pygame
import random
from modules.settings import AURORABOREALIS_SIZE, AURORABOREALIS_COLOR  # Ensure these are defined in settings.py

class AuroraBorealis:
    """
    Represents an Aurora Borealis in the game.
    Handles movement and rendering.
    """
    
    def __init__(self, screen_width, screen_height):
        self.image = pygame.Surface((AURORABOREALIS_SIZE, AURORABOREALIS_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, AURORABOREALIS_COLOR, (AURORABOREALIS_SIZE//2, AURORABOREALIS_SIZE//2), AURORABOREALIS_SIZE//2)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width + 200
        self.rect.y = random.randint(0, screen_height - AURORABOREALIS_SIZE)
        self.speed = 5  # Adjust as needed
    
    def update(self):
        """Moves the Aurora Borealis to the left based on its speed."""
        self.rect.x -= self.speed
    
    def draw(self, screen):
        """Draws the Aurora Borealis on the screen."""
        screen.blit(self.image, self.rect)
    
    def off_screen(self):
        """Checks if the Aurora Borealis has moved off the screen."""
        return self.rect.right < 0

def create_quantum_element(screen_width, screen_height):
    """Factory function to create an AuroraBorealis instance."""
    return AuroraBorealis(screen_width, screen_height)
