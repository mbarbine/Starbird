import pygame
import random
from settings import *


def dark_side_choice():
    font = pygame.font.Font(None, 40)
    prompt = "Do you embrace the Dark Side? (Y/N)"
    text_surface = font.render(prompt, True, RED)
    screen.blit(text_surface, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    
    decision_made = False
    while not decision_made:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    decision_made = True
                    return True
                elif event.key == pygame.K_n:
                    decision_made = True
                    return False
    return False



#\\ ntegration 


#from dark_side import dark_side_choice

#def random_dark_side_event():
#    if random.randint(0, 100) < 5:  # 5% chance to trigger
#        if dark_side_choice():
#            # Dark Side powers
#            obstacle_speed += 2
#            activate_force_push(obstacles)
#        else:
#            # Light Side bonus
#            activate_force_shield(bird)

# Trigger random Dark Side temptation
#random_dark_side_event()


