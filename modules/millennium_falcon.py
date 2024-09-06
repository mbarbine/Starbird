import pygame
import time
from settings import *
def millennium_falcon_assist(obstacles, duration=5):
    falcon_image = pygame.image.load('assets/millennium_falcon.png')
    falcon_rect = falcon_image.get_rect()
    falcon_rect.x = WIDTH
    falcon_rect.y = HEIGHT // 2
    
    start_time = time.time()
    while time.time() - start_time < duration:
        falcon_rect.x -= 10
        for top_obstacle, bottom_obstacle in obstacles:
            if falcon_rect.colliderect(top_obstacle):
                top_obstacle.height = 0
            if falcon_rect.colliderect(bottom_obstacle):
                bottom_obstacle.height = 0
        screen.blit(falcon_image, falcon_rect)
        pygame.display.flip()
        pygame.time.wait(50)




