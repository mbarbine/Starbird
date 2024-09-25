# levels/level2.py
import pygame
import random
from modules.quantum_effects import QuantumElement
import modules.settings as settings

# Level-specific configurations
LEVEL_BACKGROUND = 'assets/level2_bg.png'
OBSTACLE_SPEED = 4  # Increased speed for more challenge
OBSTACLE_WIDTH = 70  # Adjust width for variety
OBSTACLE_COLOR = (255, 100, 100)  # Distinct color for level obstacles
PIPE_GAP = 180  # Gap between top and bottom obstacles

QUANTUM_PROBABILITY = 0.15
BLACK_HOLE_RADIUS = 50
AURORA_RADIUS = 60

def add_obstacle(obstacles, width, height, gap_size=PIPE_GAP):
    """
    Adds a new set of top and bottom obstacles to the obstacles list.
    
    Args:
        obstacles (list): List of current obstacles in the game.
        width (int): Width of the screen.
        height (int): Height of the screen.
        gap_size (int): Size of the gap between top and bottom obstacles.
    """
    top_height = random.randint(50, height - gap_size - 50)
    bottom_height = height - gap_size - top_height

    top_obstacle = pygame.Rect(width, 0, OBSTACLE_WIDTH, top_height)
    bottom_obstacle = pygame.Rect(width, height - bottom_height, OBSTACLE_WIDTH, bottom_height)

    # Set additional attributes like color and speed to each obstacle (if needed)
    top_obstacle.color = OBSTACLE_COLOR
    top_obstacle.speed = OBSTACLE_SPEED

    bottom_obstacle.color = OBSTACLE_COLOR
    bottom_obstacle.speed = OBSTACLE_SPEED

    obstacles.append((top_obstacle, bottom_obstacle))

def spawn_quantum_element(width, height):
    """
    Spawns a new quantum element at a random position within the screen bounds.

    Args:
        width (int): Width of the screen.
        height (int): Height of the screen.

    Returns:
        QuantumElement: A new quantum element object.
    """
    return QuantumElement.spawn_random(width, height, BLACK_HOLE_RADIUS, AURORA_RADIUS)

def configure_level():
    """
    Configures and returns level-specific settings.

    Returns:
        dict: Configuration settings for Level 2.
    """
    return {
        'background_image': LEVEL_BACKGROUND,
        'obstacle_speed': OBSTACLE_SPEED,
        'obstacle_gap': PIPE_GAP,
        'quantum_probability': QUANTUM_PROBABILITY,
        'black_hole_radius': BLACK_HOLE_RADIUS,
        'aurora_radius': AURORA_RADIUS,
        'obstacle_width': OBSTACLE_WIDTH,
        'obstacle_color': OBSTACLE_COLOR
    }
