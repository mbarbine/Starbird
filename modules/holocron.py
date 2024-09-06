import pygame
import random
from settings import *
class Holocron:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load('assets/holocron.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

    def collect(self, bird):
        if self.rect.colliderect(bird):
            self.collected = True
            return True
        return False



#from holocron import Holocron

# Initialize Holocron
#holocron = Holocron(WIDTH, HEIGHT)

#def check_holocron_collection():
#    if holocron.collect(bird):
#        activate_force_shield(bird)  # Example bonus on collection

# In the game loop, draw and check for Holocron collection
#holocron.draw(screen)
#check_holocron_collection()



