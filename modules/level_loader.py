# modules/level_loader.py

import pygame
import logging
import random  # Import random for selecting pipe colors
from modules.settings import WIDTH, HEIGHT, PIPE_HEIGHT, PIPE_VARIANT_COLORS, PIPE_SPEED, PIPE_GAP, LEVEL_THRESHOLD  # Import necessary constants
from modules.pipe import Pipe
from modules.holocron import Holocron  # Assuming Holocron is defined in your project

def load_level(level_number):
    """
    Loads the level configuration based on the level number.

    Args:
        level_number (int): The current level number.

    Returns:
        dict: Level configuration settings.
    """
    # Placeholder implementation: Define level configurations manually
    level_configs = {
        1: {
            'background_path': 'assets/background_level1.png',
            'pipe_spawn_rate_frames': 90,
            'pipe_speed': 5,
            'quantum_probability': 0.01,
        },
        2: {
            'background_path': 'assets/background_level2.png',
            'pipe_spawn_rate_frames': 80,
            'pipe_speed': 6,
            'quantum_probability': 0.015,
        },
        # Add more levels as needed
    }

    if level_number in level_configs:
        logging.info(f"Level {level_number} loaded.")
        return level_configs[level_number]
    else:
        logging.warning(f"Level {level_number} not found. Loading default level.")
        return level_configs[1]

def get_level_background(level_config):
    """
    Retrieves the background path from the level configuration.

    Args:
        level_config (dict): The level configuration.

    Returns:
        str: Path to the background image.
    """
    return level_config.get('background_path', 'assets/background.png')

def add_initial_obstacles(level_config):
    """
    Adds initial obstacles based on the level configuration.

    Args:
        level_config (dict): The level configuration.

    Returns:
        list: List of initial Pipe objects.
    """
    obstacles = []
    pipe_speed = level_config.get('pipe_speed', PIPE_SPEED)  # Use default PIPE_SPEED if not in level config

    for i in range(3):  # Starting with 3 pipes
        x = WIDTH + i * 300
        pipe = Pipe(x, pipe_speed, PIPE_GAP)
        obstacles.append(pipe)

    return obstacles

def add_obstacle(level_config, obstacles, screen_width):
    """
    Adds a new pair of obstacles.

    Args:
        level_config (dict): The level configuration.
        obstacles (list): Existing list of obstacles.
        screen_width (int): Width of the game screen.
    """
    pipe_speed = level_config.get('pipe_speed', PIPE_SPEED)
    pipe = Pipe(screen_width, pipe_speed, PIPE_GAP)
    obstacles.append(pipe)

def spawn_quantum_element(level_config, screen_width, screen_height):
    """
    Spawns a quantum element based on probability.

    Args:
        level_config (dict): The level configuration.
        screen_width (int): Width of the game screen.
        screen_height (int): Height of the game screen.

    Returns:
        QuantumElement or None: The spawned quantum element or None if not spawned.
    """
    quantum_probability = level_config.get('quantum_probability', 0.01)
    if random.random() < quantum_probability:
        return Holocron(screen_width, screen_height)
    return None

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
        tuple: Updated (current_level, background, level_config)
    """
    if score != 0 and score % LEVEL_THRESHOLD == 0:
        current_level += 1
        logging.info(f"Progressing to level {current_level}.")
        try:
            new_level_config = load_level(current_level)
        except Exception as e:
            logging.error(f"Failed to load level {current_level}: {e}")
            return current_level, background, level_config

        new_obstacles = add_initial_obstacles(new_level_config)
        if new_obstacles:
            obstacles.extend(new_obstacles)
            logging.info(f"Added {len(new_obstacles)} new obstacles for level {current_level}.")

        new_background_path = get_level_background(new_level_config)
        if new_background_path:
            background.load_new_background(new_background_path)
            logging.info(f"Background updated for level {current_level}.")

        # Increase difficulty
        global PIPE_SPEED
        PIPE_SPEED += 0.5  # Increase speed by 0.5 each level
        global PIPE_SPAWN_RATE_FRAMES
        PIPE_SPAWN_RATE_FRAMES = max(30, new_level_config.get('pipe_spawn_rate_frames', 30) - 10)  # Adjust spawn rate

        return current_level, background, new_level_config
    else:
        return current_level, background, level_config
