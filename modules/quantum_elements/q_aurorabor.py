# modules/quantum_elements/q_aurorabor.py

import os
import pygame
import random
import logging

def create_quantum_element(screen_width, screen_height):
    """
    Creates an Aurora Borealis quantum element.
    
    Args:
        screen_width (int): Width of the game screen.
        screen_height (int): Height of the game screen.
    
    Returns:
        AuroraBorealis: An instance of the AuroraBorealis class.
    """
    return AuroraBorealis(screen_width, screen_height)

class AuroraBorealis:
    def __init__(self, screen_width, screen_height):
        # Determine the absolute path to the image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, '..', '..', 'assets', 'AuroraBorealis.png')
        
        # Normalize the path
        image_path = os.path.normpath(image_path)
        
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            logging.info(f"AuroraBorealis image loaded from {image_path}.")
        except pygame.error as e:
            logging.error(f"Failed to load AuroraBorealis image from {image_path}: {e}")
            # Load a default image or handle the error as needed
            self.image = pygame.Surface((50, 50))  # Placeholder surface
            self.image.fill((0, 255, 0))  # Green square as a placeholder
        
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.speed = 3
    
    def update(self):
        self.rect.x -= self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def off_screen(self):
        return self.rect.x < -self.rect.width
