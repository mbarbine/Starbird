# backgrounds.py

import pygame
import logging

class ScrollingBackground:
    """
    A class to create a horizontally scrolling background in Pygame.
    """

    def __init__(self, background_path='./assets/background.png', speed=2):
        """
        Initializes the scrolling background with a specified image and speed.

        Args:
            background_path (str): The path to the background image.
            speed (int): The speed at which the background scrolls.
        """
        self.speed = speed
        self.image = None
        self.rect1 = None
        self.rect2 = None

        # Load the initial background image
        self.load_new_background(background_path)

    def load_new_background(self, background_path):
        """
        Loads a new background image and resets the scrolling.

        Args:
            background_path (str): The path to the new background image.
        """
        try:
            self.image = pygame.image.load(background_path).convert()
            self.rect1 = self.image.get_rect()
            self.rect2 = self.image.get_rect()
            self.rect2.x = self.rect1.width
            logging.info(f"Background updated from {background_path}.")
        except pygame.error as e:
            logging.error(f"Failed to load new background image: {e}")
            self.image = None

    def update(self):
        """
        Updates the position of the background for scrolling effect.
        """
        if self.image:
            self.rect1.x -= self.speed
            self.rect2.x -= self.speed

            # Wrap the background images around
            if self.rect1.right <= 0:
                self.rect1.x = self.rect2.right
            if self.rect2.right <= 0:
                self.rect2.x = self.rect1.right

    def draw(self, screen):
        """
        Draws the scrolling background onto the given screen.

        Args:
            screen (pygame.Surface): The screen surface to draw the background on.
        """
        if self.image:
            screen.blit(self.image, self.rect1)
            screen.blit(self.image, self.rect2)
        else:
            logging.warning("No background image to draw.")

    def change_speed(self, new_speed):
        """
        Changes the scrolling speed of the background.

        Args:
            new_speed (int): The new scrolling speed.
        """
        self.speed = new_speed
        logging.info(f"Background scrolling speed set to {new_speed}.")
