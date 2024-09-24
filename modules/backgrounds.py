# modules/backgrounds.py

import pygame
import random
import os
import logging
from modules.settings import *

class ScrollingBackground:
    """
    Handles the scrolling background with parallax effect and additional effects like stars and comets.
    """
    def __init__(self):
        """Initializes the scrolling background with parallax and additional effects."""
        self.layers = []
        self.positions = []
        self.scroll_speeds = []
        self.paused = False

        # Load primary background image
        self.image = pygame.image.load(os.path.join('assets', BACKGROUND_IMAGE)).convert()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x1 = 0
        self.x2 = self.width
        self.y = 0

        # Load additional background layers from settings (optional)
        try:
            for i, layer_filename in enumerate(BACKGROUND_LAYERS):
                layer_path = os.path.join('assets', layer_filename)
                layer_image = pygame.image.load(layer_path).convert_alpha()
                self.layers.append(layer_image)
                self.positions.append(0)
                self.scroll_speeds.append(BACKGROUND_SCROLL_SPEED * (i + 1))
            logging.info("Background layers loaded successfully.")
        except pygame.error as e:
            logging.error(f"Error loading background layers: {e}")
            self.layers = []

        # Starfield effect settings
        self.stars = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(STAR_COUNT)]
        self.star_color = STAR_COLOR
        self.star_speed = STAR_SPEED

        # Comet effect settings
        self.comet_position = [-100, random.randint(0, self.height)]
        self.comet_speed = COMET_SPEED
        self.comet_color = COMET_COLOR

    def update(self, dt):
        """Updates the position of each background layer and visual effects based on delta time."""
        if self.paused:
            return  # Skip updating if paused

        # Update main background scroll positions
        self.x1 -= BACKGROUND_SCROLL_SPEED * dt * 60
        self.x2 -= BACKGROUND_SCROLL_SPEED * dt * 60

        if self.x1 <= -self.width:
            self.x1 = self.width
        if self.x2 <= -self.width:
            self.x2 = self.width

        # Update additional background layers (if present)
        for i, speed in enumerate(self.scroll_speeds):
            self.positions[i] -= speed * dt * 60
            if self.positions[i] <= -WIDTH:
                self.positions[i] += WIDTH

        # Update star positions for starfield effect
        self.update_stars()

        # Update comet position
        self.update_comet()

    def update_stars(self):
        """Updates the star positions for the starfield effect."""
        for i in range(len(self.stars)):
            x, y = self.stars[i]
            x -= self.star_speed
            if x < 0:
                x = self.width
                y = random.randint(0, self.height)
            self.stars[i] = (x, y)

    def update_comet(self):
        """Updates the position of the comet."""
        self.comet_position[0] += self.comet_speed[0]
        self.comet_position[1] += self.comet_speed[1]
        if self.comet_position[0] > self.width or self.comet_position[1] > self.height:
            self.comet_position = [-100, random.randint(0, self.height)]

    def draw(self, screen):
        """Draws all background layers, starfield, comet, and black hole onto the screen."""
        # Draw the main scrolling background image
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))

        # Draw additional background layers (if present)
        for i, layer in enumerate(self.layers):
            screen.blit(layer, (self.positions[i], 0))
            screen.blit(layer, (self.positions[i] + WIDTH, 0))

        # Draw the starfield effect
        self.draw_stars(screen)

        # Draw the comet
        self.draw_comet(screen)

        # Draw the black hole effect if enabled
        if DRAW_BLACK_HOLE:
            self.draw_black_hole(screen)

    def draw_stars(self, screen):
        """Draws the stars for the starfield effect."""
        for x, y in self.stars:
            screen.set_at((x, y), self.star_color)

    def draw_comet(self, screen):
        """Draws the comet."""
        pygame.draw.circle(screen, self.comet_color, self.comet_position, COMET_SIZE)

    def draw_black_hole(self, screen):
        """Draws a black hole at the center of the screen."""
        pygame.draw.circle(screen, BLACK_HOLE_COLOR, (self.width // 2, self.height // 2), BLACK_HOLE_RADIUS)

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
        """Changes the scrolling speed of all background layers."""
        self.scroll_speeds = [new_speed * (i + 1) for i in range(len(self.layers))]
        logging.info(f"Background scrolling speed set to {new_speed}.")

    def set_layer_speed(self, layer_index, speed_multiplier):
        """Sets a custom scrolling speed multiplier for a specific layer."""
        if 0 <= layer_index < len(self.layers):
            self.scroll_speeds[layer_index] = BACKGROUND_SCROLL_SPEED * (layer_index + 1) * speed_multiplier
            logging.info(f"Layer {layer_index} speed set to {self.scroll_speeds[layer_index]}.")
        else:
            logging.error(f"Invalid layer index: {layer_index}.")

    def reset(self):
        """Resets all background layers and scroll positions."""
        self.positions = [0 for _ in self.layers]
        self.scroll_speeds = [BACKGROUND_SCROLL_SPEED * (i + 1) for i in range(len(self.layers))]
        logging.info("Background layers and positions reset.")

    def remove_layer(self, layer_index):
        """Removes a background layer at the specified index."""
        if 0 <= layer_index < len(self.layers):
            del self.layers[layer_index]
            del self.positions[layer_index]
            del self.scroll_speeds[layer_index]
            logging.info(f"Layer {layer_index} removed.")
        else:
            logging.error(f"Invalid layer index: {layer_index}.")

    def pause(self):
        """Pauses the background scrolling."""
        self.paused = True
        logging.info("Background scrolling paused.")

    def resume(self):
        """Resumes the background scrolling."""
        self.paused = False
        logging.info("Background scrolling resumed.")
