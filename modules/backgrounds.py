# modules/backgrounds.py

import pygame
import os
import logging

class ScrollingBackground:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(self.base_path, '..', 'assets', 'background.png')).convert()
        self.rect = self.image.get_rect()
        self.scroll_speed = 2
        self.x = 0

    def update(self):
        self.x -= self.scroll_speed
        if self.x <= -self.rect.width:
            self.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, 0))
        screen.blit(self.image, (self.x + self.rect.width, 0))

    def load_new_background(self, background_path):
        full_path = os.path.join(self.base_path, '..', background_path)
        try:
            self.image = pygame.image.load(full_path).convert()
            self.rect = self.image.get_rect()
            logging.info(f"Background loaded from {full_path}.")
        except pygame.error as e:
            logging.error(f"Failed to load background from {full_path}: {e}")
            # Fallback to default background
            self.image = pygame.Surface((WIDTH, HEIGHT))
            self.image.fill((0, 0, 0))  # Black background
