# levels/level1.py
import pygame
import random
from quantum_effects import QuantumElement
from modules.pipe import Pipe  # Ensure Pipe is imported

# Level-specific configurations
LEVEL_BACKGROUND = 'assets/level1_bg.png'
OBSTACLE_SPEED = 3
QUANTUM_PROBABILITY = 0.1
BLACK_HOLE_RADIUS = 40
AURORA_RADIUS = 50
GAP_SIZE = 180  # Ensure this matches your settings

def add_obstacle(obstacles, width, height, gap_size=GAP_SIZE):
    """Creates and appends a new Pipe instance to the obstacles list."""
    top_height = random.randint(50, height - gap_size - 50)
    bottom_height = height - gap_size - top_height
    pipe = Pipe(x=width, top_height=top_height, bottom_height=bottom_height, speed=OBSTACLE_SPEED)
    obstacles.append(pipe)
    logging.debug(f"Pipe added at x={width} with top_height={top_height} and bottom_height={bottom_height}.")

def spawn_quantum_element(width, height):
    """Spawns a random QuantumElement."""
    return QuantumElement.spawn_random(width, height, BLACK_HOLE_RADIUS, AURORA_RADIUS)
