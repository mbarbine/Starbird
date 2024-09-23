# modules/quantum_elements/QBlackHole.py

import pygame
import random
import os
import logging

def create_quantum_element(screen_width, screen_height):
    """
    Creates a QBlackHole quantum element.
    
    Args:
        screen_width (int): Width of the game screen.
        screen_height (int): Height of the game screen.
    
    Returns:
        QBlackHole: An instance of the QBlackHole class.
    """
    return QBlackHole(screen_width, screen_height)


class QBlackHole:
    def __init__(self, screen_width, screen_height):
        # Construct the absolute path to the image
        base_path = os.path.dirname(__file__)  # Directory of QBlackHole.py
        image_path = os.path.join(base_path, 'QBlackHole.png')  # Adjust if in a different folder
        
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            logging.info(f"QBlackHole image loaded from {image_path}.")
        except pygame.error as e:
            logging.error(f"Failed to load QBlackHole image from {image_path}: {e}")
            # Handle the missing image scenario, e.g., load a default image or exit
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 0, 0))  # Black square as a fallback
        
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.speed = 5
    
    def update(self):
        self.rect.x -= self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def off_screen(self):
        return self.rect.x < -self.rect.width
