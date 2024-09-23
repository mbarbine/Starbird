import pygame
import time
from modules.settings import *
def activate_jedi_mind_trick(obstacles, duration=2):
    hidden_obstacles = []

    for top_obstacle, bottom_obstacle in obstacles:
        hidden_obstacles.append((top_obstacle, bottom_obstacle))
        top_obstacle.x = -100  # Move them off-screen
        bottom_obstacle.x = -100
    
    pygame.time.wait(duration * 1000)

    # Restore obstacles after duration
    for top_obstacle, bottom_obstacle in hidden_obstacles:
        top_obstacle.x += 100  # Move them back on-screen
        bottom_obstacle.x += 100


\\ integration 

from jedi_mind_trick import activate_jedi_mind_trick

def random_power_up():
    power_up_chance = np.random.randint(0, 100)
    if power_up_chance < 10:
        activate_lightsaber()
    elif power_up_chance < 20:
        activate_force_push(obstacles)
    elif power_up_chance < 30:
        activate_force_shield(bird)
    elif power_up_chance < 40:
        activate_jedi_mind_trick(obstacles)

# Call random_power_up at key moments in the game
random_power_up()


