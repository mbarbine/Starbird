# backgrounds.py

import pygame
import logging

class ScrollingBackground:
    def __init__(self, background_path='./assets/background.png'):
        try:
            self.image = pygame.image.load(background_path).convert()
            self.rect1 = self.image.get_rect()
            self.rect2 = self.image.get_rect()
            self.rect2.x = self.rect1.width
            self.speed = 2  # Adjust as needed
            logging.info(f"Background loaded from {background_path}.")
        except pygame.error as e:
            logging.error(f"Failed to load background image: {e}")
            self.image = None

    def load_new_background(self, background_path):
        try:
            self.image = pygame.image.load(background_path).convert()
            self.rect1 = self.image.get_rect()
            self.rect2 = self.image.get_rect()
            self.rect2.x = self.rect1.width
            logging.info(f"Background updated from {background_path}.")
        except pygame.error as e:
            logging.error(f"Failed to load new background image: {e}")

    def update(self):
        if self.image:
            self.rect1.x -= self.speed
            self.rect2.x -= self.speed
            if self.rect1.right <= 0:
                self.rect1.x = self.rect2.right
            if self.rect2.right <= 0:
                self.rect2.x = self.rect1.right

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect1)
            screen.blit(self.image, self.rect2)
