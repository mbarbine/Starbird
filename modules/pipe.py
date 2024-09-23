# pipe.py

import pygame
from modules.settings import PIPE_WIDTH, PIPE_COLOR, PIPE_HEIGHT, GAP_SIZE  # Ensure PIPE_COLOR is defined in settings


class Pipe:
    """
    Represents a pair of top and bottom pipes in the game.
    """
    
    def __init__(self, x, top_height, bottom_height, speed=5):
        """
        Initializes the Pipe instance.
        
        Args:
            x (int): The x-coordinate of the pipe.
            top_height (int): Height of the top pipe.
            bottom_height (int): Height of the bottom pipe.
            speed (int, optional): Movement speed of the pipe. Defaults to 5.
        """
        self.top_rect = pygame.Rect(x, 0, PIPE_WIDTH, top_height)
        self.bottom_rect = pygame.Rect(x, PIPE_HEIGHT - bottom_height, PIPE_WIDTH, bottom_height)
        self.speed = speed
        # Combined rect for collision detection (optional)
        self.rect = pygame.Rect(x, 0, PIPE_WIDTH, top_height + bottom_height + GAP_SIZE)
    
    def update(self):
        """Moves the pipe to the left based on its speed."""
        self.top_rect.x -= self.speed
        self.bottom_rect.x -= self.speed
        self.rect.x -= self.speed
    
    def draw(self, screen):
        """Draws the top and bottom pipes on the screen."""
        pygame.draw.rect(screen, PIPE_COLOR, self.top_rect)
        pygame.draw.rect(screen, PIPE_COLOR, self.bottom_rect)
    
    def off_screen(self):
        """Checks if the pipe has moved off the screen."""
        return self.top_rect.right < 0
