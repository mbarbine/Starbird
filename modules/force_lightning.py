import pygame
from settings import *

def activate_force_lightning(obstacles):
    for top_obstacle, bottom_obstacle in obstacles:
        if top_obstacle.colliderect(bird) or bottom_obstacle.colliderect(bird):
            top_obstacle.height = 0
            bottom_obstacle.height = 0
            pygame.draw.line(screen, WHITE, bird.center, top_obstacle.midbottom, 2)
            pygame.draw.line(screen, WHITE, bird.center, bottom_obstacle.midtop, 2)
            pygame.display.flip()


