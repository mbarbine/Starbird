# pipe.py

import pygame
import random  # Added import for random
from modules.settings import PIPE_WIDTH, PIPE_COLOR, PIPE_HEIGHT, PIPE_GAP  # Replaced GAP_SIZE with PIPE_GAP


class Pipe:
    """
    Represents a pair of top and bottom pipes in the game.
    """
    
    def __init__(self, x, speed, pipe_gap=PIPE_GAP):
        """
        Initializes the Pipe instance.
        
        Args:
            x (int): The x-coordinate of the pipe.
            speed (int, optional): Movement speed of the pipe. Defaults to PIPE_SPEED.
            pipe_gap (int, optional): Gap between top and bottom pipes. Defaults to PIPE_GAP.
        """
        self.speed = speed
        self.pipe_gap = pipe_gap

        # Randomize top pipe height
        top_height = random.randint(50, PIPE_HEIGHT - pipe_gap - 50)
        self.top_rect = pygame.Rect(x, 0, PIPE_WIDTH, top_height)

        # Bottom pipe height is determined based on the gap
        bottom_height = PIPE_HEIGHT - top_height - pipe_gap
        self.bottom_rect = pygame.Rect(x, PIPE_HEIGHT - bottom_height, PIPE_WIDTH, bottom_height)

        # Combined rect for collision detection (optional)
        self.rect = pygame.Rect(x, 0, PIPE_WIDTH, top_height + bottom_height + pipe_gap)
    
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
