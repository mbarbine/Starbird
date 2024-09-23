import pygame
from modules.settings import *
import random

class ScrollingBackground:
    def __init__(self):
        # Load the background image
        self.image = pygame.image.load(BACKGROUND_IMAGE).convert()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x1 = 0
        self.x2 = self.width
        self.y = 0

        # Starfield effect
        self.stars = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(100)]
        self.star_color = (255, 255, 255)
        self.star_speed = 2

        # Comet effect
        self.comet_position = [-100, random.randint(0, self.height)]
        self.comet_speed = [5, 1]
        self.comet_color = (255, 255, 0)

    def update(self):
        self.x1 -= BACKGROUND_SCROLL_SPEED
        self.x2 -= BACKGROUND_SCROLL_SPEED

        if self.x1 <= -self.width:
            self.x1 = self.width
        if self.x2 <= -self.width:
            self.x2 = self.width

        # Update star positions for starfield effect
        self.update_stars()

        # Update comet position
        self.update_comet()

    def update_stars(self):
        for i in range(len(self.stars)):
            x, y = self.stars[i]
            x -= self.star_speed
            if x < 0:
                x = self.width
                y = random.randint(0, self.height)
            self.stars[i] = (x, y)

    def update_comet(self):
        self.comet_position[0] += self.comet_speed[0]
        self.comet_position[1] += self.comet_speed[1]
        if self.comet_position[0] > self.width or self.comet_position[1] > self.height:
            self.comet_position = [-100, random.randint(0, self.height)]

    def draw(self, screen):
        # Draw the scrolling background image
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))

        # Draw the starfield effect
        self.draw_stars(screen)

        # Draw the comet
        self.draw_comet(screen)

        # Draw the black hole
        pygame.draw.circle(screen, BLACK_HOLE_COLOR, (self.width // 2, self.height // 2), BLACK_HOLE_RADIUS)

    def draw_stars(self, screen):
        for x, y in self.stars:
            screen.set_at((x, y), self.star_color)

    def draw_comet(self, screen):
        pygame.draw.circle(screen, self.comet_color, self.comet_position, 10)
