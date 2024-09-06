# levels/level1.py
import pygame
import random
from quantum_effects import QuantumElement

# Level-specific configurations
LEVEL_BACKGROUND = 'assets/level1_bg.png'
OBSTACLE_SPEED = 3
QUANTUM_PROBABILITY = 0.1
BLACK_HOLE_RADIUS = 40
AURORA_RADIUS = 50

def add_obstacle(obstacles, width, height, gap_size):
    top_height = random.randint(50, height - gap_size - 50)
    bottom_height = height - gap_size - top_height
    top_obstacle = pygame.Rect(width, 0, 50, top_height)
    bottom_obstacle = pygame.Rect(width, height - bottom_height, 50, bottom_height)
    obstacles.append((top_obstacle, bottom_obstacle))

def spawn_quantum_element(width, height):
    return QuantumElement.spawn_random(width, height, BLACK_HOLE_RADIUS, AURORA_RADIUS)
