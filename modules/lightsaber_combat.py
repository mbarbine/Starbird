import pygame
from settings import *
def lightsaber_duel(event):
    success = False
    if event.key == pygame.K_LEFT:
        print("Block left!")
        success = True
    elif event.key == pygame.K_RIGHT:
        print("Block right!")
        success = True
    elif event.key == pygame.K_UP:
        print("Attack!")
        success = True
    else:
        print("Missed!")
    
    return success



