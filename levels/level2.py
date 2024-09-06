# levels/level2.py
import pygame
import random
from quantum_effects import QuantumElement

# Level-specific configurations
LEVEL_BACKGROUND = 'assets/level2_bg.png'
OBSTACLE_SPEED = 4  # Increased speed for more challenge
QUANTUM_PROBABILITY = 0.15
BLACK_HOLE_RADIUS = 50
AURORA_RADIUS = 60

def add_obstacle(obstacles, width, height, gap_size):
    top_height = random.randint(50, height - gap_size - 50)
    bottom_height = height - gap_size - top_height
    top_obstacle = pygame.Rect(width, 0, 50, top_height)
    bottom_obstacle = pygame.Rect(width, height - bottom_height, 50, bottom_height)
    obstacles.append((top_obstacle, bottom_obstacle))

def spawn_quantum_element(width, height):
    return QuantumElement.spawn_random(width, height, BLACK_HOLE_RADIUS, AURORA_RADIUS)
