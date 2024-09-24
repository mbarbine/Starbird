import pygame
import random
from modules.settings import *

def starship_flyby(screen):
    starship_image = pygame.image.load('assets/starship.png')
    starship_image = pygame.transform.scale(starship_image, (100, 50))
    
    start_x = WIDTH
    start_y = random.randint(0, HEIGHT - 50)
    
    for i in range(WIDTH + 100):
        screen.blit(starship_image, (start_x - i, start_y))
        pygame.display.flip()
        pygame.time.wait(10)

from starship_flyby import starship_flyby

def random_visual_effect():
    visual_chance = np.random.randint(0, 100)
    if visual_chance < 10:
        starship_flyby(screen)

# Call random_visual_effect at random moments
random_visual_effect()


