# levels/level1.py

import pygame
import random
import logging
from quantum_effects import QuantumElement
from modules.pipe import Pipe
from modules.settings import PIPE_SPEED, PIPE_GAP, BLACK_HOLE_RADIUS, AURORA_RADIUS, HEIGHT, PIPE_VARIANT_COLORS

# Level-specific configurations
LEVEL_BACKGROUND = 'assets/level1_bg.png'
OBSTACLE_SPEED = PIPE_SPEED  # Use PIPE_SPEED from settings
GAP_SIZE = PIPE_GAP  # Use PIPE_GAP from settings
QUANTUM_PROBABILITY = 0.1  # Can override from settings if needed

def add_obstacle(obstacles, width, height=HEIGHT, gap_size=GAP_SIZE):
    """Creates and appends a new Pipe instance to the obstacles list."""
    top_height = random.randint(50, height - gap_size - 50)
    bottom_height = height - gap_size - top_height
    
    # Using the Pipe class directly
    pipe = Pipe(x=width, speed=OBSTACLE_SPEED, pipe_gap=gap_size)
    pipe.color = random.choice(PIPE_VARIANT_COLORS)  # Set random color for variety
    obstacles.append(pipe)
    logging.debug(f"Pipe added at x={width} with top_height={top_height} and bottom_height={bottom_height}.")

def spawn_quantum_element(width, height):
    """Spawns a random QuantumElement."""
    return QuantumElement.spawn_random(width, height, BLACK_HOLE_RADIUS, AURORA_RADIUS)
