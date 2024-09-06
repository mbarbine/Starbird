import pygame
import time
from settings import *

def activate_force_shield(bird, duration=3):
    shield_on = True
    start_time = time.time()
    
    while shield_on:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            shield_on = False
        
        pygame.draw.circle(screen, BLUE, bird.center, bird.width + 10, 2)
        pygame.display.flip()
        pygame.time.wait(50)

