# modules/level_manager.py

import pygame
import logging
import random
from modules.settings import (
    WIDTH, HEIGHT, PIPE_HEIGHT, PIPE_VARIANT_COLORS, PIPE_SPEED, 
    PIPE_GAP, LEVEL_THRESHOLD, PIPE_SPAWN_RATE_FRAMES, BLACK_HOLE_RADIUS, AURORA_RADIUS
)
from modules.pipe import Pipe
from modules.holocron import Holocron
from modules.backgrounds import ScrollingBackground

# Level Configuration Dictionary
LEVEL_CONFIGS = {
    1: {
        'background_path': 'assets/background_level1.png',
        'pipe_spawn_rate_frames': 90,
        'pipe_speed': 5,
        'quantum_probability': 0.01,
        'num_initial_obstacles': 3,
        'obstacle_gap_reduction_rate': 5,
        'quantum_element_type': 'holocron'
    },
    2: {
        'background_path': 'assets/background_level2.png',
        'pipe_spawn_rate_frames': 80,
        'pipe_speed': 6,
        'quantum_probability': 0.015,
        'num_initial_obstacles': 4,
        'obstacle_gap_reduction_rate': 10,
        'quantum_element_type': 'black_hole'
    },
    # Additional levels can be configured here
}

def load_level(level_number):
    """
    Loads the level configuration based on the level number.

    Args:
        level_number (int): The current level number.

    Returns:
        dict: Level configuration settings.
    """
    if level_number in LEVEL_CONFIGS:
        logging.info(f"Level {level_number} loaded.")
        return LEVEL_CONFIGS[level_number]
    else:
        logging.warning(f"Level {level_number} not found. Loading default level configuration.")
        return default_level_config()

def default_level_config():
    """
    Returns a default level configuration if no specific level config is found.

    Returns:
        dict: Default configuration for the level.
    """
    logging.info("Using default level configuration.")
    return {
        'background_path': 'assets/background_default.png',
        'pipe_spawn_rate_frames': 100,
        'pipe_speed': 4,
        'quantum_probability': 0.01,
        'num_initial_obstacles': 3,
        'obstacle_gap_reduction_rate': 5,
        'quantum_element_type': 'holocron'
    }

def get_level_background(level_config):
    """
    Retrieves the background path from the level configuration.

    Args:
        level_config (dict): The level configuration.

    Returns:
        str: Path to the background image.
    """
    return level_config.get('background_path', 'assets/background_default.png')

def add_initial_obstacles(level_config):
    """
    Adds initial obstacles based on the level configuration.

    Args:
        level_config (dict): The level configuration.

    Returns:
        list: List of initial Pipe objects.
    """
    obstacles = []
    num_obstacles = level_config.get('num_initial_obstacles', 3)
    pipe_speed = level_config.get('pipe_speed', PIPE_SPEED)
    gap_size = level_config.get('pipe_gap', PIPE_GAP)
    
    for i in range(num_obstacles):
        x = WIDTH + i * 300
        pipe = Pipe(x, pipe_speed, gap_size)
        obstacles.append(pipe)
    
    logging.info(f"Added {num_obstacles} initial obstacles.")
    return obstacles

def add_obstacle(level_config, obstacles, screen_width):
    """
    Adds a new pair of obstacles to the game.

    Args:
        level_config (dict): The level configuration.
        obstacles (list): Existing list of obstacles.
        screen_width (int): Width of the game screen.
    """
    pipe_speed = level_config.get('pipe_speed', PIPE_SPEED)
    pipe_gap = level_config.get('pipe_gap', PIPE_GAP)
    pipe = Pipe(screen_width, pipe_speed, pipe_gap)
    obstacles.append(pipe)
    logging.info(f"New obstacle added at x={screen_width}.")

def spawn_quantum_element(level_config, screen_width, screen_height):
    """
    Spawns a quantum element based on the level configuration.

    Args:
        level_config (dict): The level configuration.
        screen_width (int): Width of the game screen.
        screen_height (int): Height of the game screen.

    Returns:
        QuantumElement or None: The spawned quantum element or None if not spawned.
    """
    quantum_probability = level_config.get('quantum_probability', 0.01)
    quantum_element_type = level_config.get('quantum_element_type', 'holocron')
    
    if random.random() < quantum_probability:
        if quantum_element_type == 'holocron':
            return Holocron(screen_width, screen_height)
        elif quantum_element_type == 'black_hole':
            return create_black_hole(screen_width, screen_height)
        elif quantum_element_type == 'aurora':
            return create_aurora(screen_width, screen_height)
        else:
            logging.warning(f"Unknown quantum element type: {quantum_element_type}. No element spawned.")
            return None
    return None

def create_black_hole(screen_width, screen_height):
    """
    Creates a black hole quantum element.

    Args:
        screen_width (int): Width of the screen.
        screen_height (int): Height of the screen.

    Returns:
        dict: Dictionary representing the black hole element.
    """
    x_position = random.randint(50, screen_width - 50)
    y_position = random.randint(50, screen_height - 50)
    return {
        'type': 'black_hole',
        'x_position': x_position,
        'y_position': y_position,
        'radius': BLACK_HOLE_RADIUS,
        'color': (0, 0, 0)
    }

def create_aurora(screen_width, screen_height):
    """
    Creates an aurora quantum element.

    Args:
        screen_width (int): Width of the screen.
        screen_height (int): Height of the screen.

    Returns:
        dict: Dictionary representing the aurora element.
    """
    x_position = random.randint(50, screen_width - 50)
    y_position = random.randint(50, screen_height - 50)
    return {
        'type': 'aurora',
        'x_position': x_position,
        'y_position': y_position,
        'radius': AURORA_RADIUS,
        'color': (0, 255, 255)
    }

def handle_level_progression(score, current_level, background, screen, obstacles, level_config):
    """
    Handles level progression based on the score.

    Args:
        score (int): Current score.
        current_level (int): Current level number.
        background (ScrollingBackground): The background object.
        screen (pygame.Surface): The game screen.
        obstacles (list): List of current obstacles.
        level_config (dict): Current level configuration.

    Returns:
        tuple: Updated (current_level, background, level_config).
    """
    if score != 0 and score % LEVEL_THRESHOLD == 0:
        current_level += 1
        logging.info(f"Progressing to level {current_level}.")
        try:
            new_level_config = load_level(current_level)
        except Exception as e:
            logging.error(f"Failed to load level {current_level}: {e}")
            return current_level, background, level_config

        # Add new obstacles based on the new level config
        new_obstacles = add_initial_obstacles(new_level_config)
        if new_obstacles:
            obstacles.extend(new_obstacles)
            logging.info(f"Added {len(new_obstacles)} new obstacles for level {current_level}.")

        # Update background for new level
        new_background_path = get_level_background(new_level_config)
        if new_background_path:
            background.load_new_background(new_background_path)
            logging.info(f"Background updated for level {current_level}.")

        # Increase game difficulty (speed, spawn rate, etc.)
        global PIPE_SPEED, PIPE_SPAWN_RATE_FRAMES
        PIPE_SPEED = new_level_config.get('pipe_speed', PIPE_SPEED) + 0.5
        PIPE_SPAWN_RATE_FRAMES = max(30, new_level_config.get('pipe_spawn_rate_frames', 30) - 10)
        logging.info(f"Updated game difficulty: Pipe Speed={PIPE_SPEED}, Spawn Rate Frames={PIPE_SPAWN_RATE_FRAMES}.")

        return current_level, background, new_level_config
    else:
        return current_level, background, level_config
