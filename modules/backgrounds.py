# modules/backgrounds.py

import pygame
import logging
import os
from modules.settings import *

class ScrollingBackground:
    """
    Handles the scrolling background with parallax effect.
    """
    def __init__(self):
        """Initializes the scrolling background."""
        self.layers = []
        self.positions = []
        self.scroll_speeds = []
        
        # Load background layers from settings
        try:
            for i, layer_filename in enumerate(BACKGROUND_LAYERS):
                # Ensure the layer path includes the assets directory
                layer_path = os.path.join('assets', layer_filename)
                layer_image = pygame.image.load(layer_path).convert_alpha()
                self.layers.append(layer_image)
                self.positions.append(0)
                # Assign scroll speeds for parallax (closer layers scroll faster)
                self.scroll_speeds.append(BACKGROUND_SCROLL_SPEED * (i + 1))
            logging.info("Background layers loaded successfully.")
        except pygame.error as e:
            logging.error(f"Error loading background layers: {e}")
            # Create placeholder surfaces if loading fails
            for _ in BACKGROUND_LAYERS:
                layer = pygame.Surface((WIDTH, HEIGHT))
                layer.fill(BACKGROUND_COLOR)
                self.layers.append(layer)
                self.positions.append(0)
                self.scroll_speeds.append(BACKGROUND_SCROLL_SPEED)
        
    def update(self, dt):
        """
        Updates the position of each background layer based on delta time.
        
        Args:
            dt (float): Time elapsed since the last frame in seconds.
        """
        for i, speed in enumerate(self.scroll_speeds):
            self.positions[i] -= speed * dt * 60  # Scale speed with dt (assuming 60 FPS baseline)
            if self.positions[i] <= -WIDTH:
                self.positions[i] = 0  # Reset position to loop the background
    
    def draw(self, screen):
        """
        Draws all background layers onto the screen.
        
        Args:
            screen (pygame.Surface): The game screen surface.
        """
        for i, layer in enumerate(self.layers):
            # Draw the layer twice for seamless scrolling
            screen.blit(layer, (self.positions[i], 0))
            screen.blit(layer, (self.positions[i] + WIDTH, 0))
    
    def load_new_background(self, layer_filename):
        """
        Loads a new background layer.
        
        Args:
            layer_filename (str): The filename of the new background image.
        """
        try:
            layer_path = os.path.join('assets', layer_filename)
            layer_image = pygame.image.load(layer_path).convert_alpha()
            self.layers.append(layer_image)
            self.positions.append(0)
            self.scroll_speeds.append(BACKGROUND_SCROLL_SPEED * (len(self.layers)))
            logging.info(f"New background layer loaded from {layer_filename}.")
        except pygame.error as e:
            logging.error(f"Failed to load new background layer '{layer_filename}': {e}")
    
    def change_speed(self, new_speed):
        """
        Changes the scrolling speed of all background layers.
    
        Args:
            new_speed (float): The new scrolling speed multiplier.
        """
        self.scroll_speeds = [new_speed * (i + 1) for i in range(len(self.layers))]
        logging.info(f"Background scrolling speed set to {new_speed}.")
