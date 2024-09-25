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
    return QuantumElement.spawn_random(width, height, BLACK_HOLE_RADIUS, AURORA_RADIUS) - level_config - {
    "level1": {
        "background": "assets/background_level1.png",
        "obstacle_speed": 5,
        "obstacle_type": "pipe",
        "num_obstacles": 3,
        "quantum_probability": 0.1,
        "quantum_element": "QBlackHole",
        "gap_size": 180,
        "pipe_variants": [
            [34, 139, 34],
            [107, 142, 35],
            [154, 205, 50]
        ]
    },
    "level2": {
        "level_number": 2,
        "background_image": "assets/level2_bg.png",
        "obstacle_speed": 4,
        "obstacle_width": 70,
        "obstacle_gap": 180,
        "quantum_probability": 0.15,
        "black_hole_radius": 50,
        "aurora_radius": 60,
        "obstacle_color": [255, 100, 100],
        "max_obstacles": 5,
        "quantum_spawn_interval": 10,
        "difficulty_scale": 1.2
      }
    }
      
