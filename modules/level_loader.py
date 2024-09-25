# modules/level_loader.py

import json
import logging
import os
import random
from modules.settings import (
    PIPE_SPEED, PIPE_GAP, BLACK_HOLE_RADIUS, AURORA_RADIUS,
    LEVEL_THRESHOLD, PIPE_SPAWN_RATE_FRAMES, PIPE_VARIANT_COLORS,
    WIDTH, HEIGHT
)
from modules.pipe import Pipe
from modules.backgrounds import ScrollingBackground

def load_level(level_number):
    """
    Loads the level configuration from a JSON file.

    Args:
        level_number (int): The current level number to load.

    Returns:
        dict: A dictionary containing the level configuration.
    """
    level_file_path = os.path.join('levels', 'level_config.json')
    try:
        if not os.path.exists(level_file_path):
            logging.error(f"Level configuration file {level_file_path} does not exist.")
            return default_level_config()

        with open(level_file_path, 'r') as file:
            level_data = json.load(file)
            level_key = f'level{level_number}'
            if level_key in level_data:
                level_config = level_data[level_key]
                logging.info(f"Level {level_number} configuration loaded successfully.")
                return level_config
            else:
                logging.warning(f"Level {level_number} configuration not found. Using default settings.")
                return default_level_config()
    except json.JSONDecodeError as json_err:
        logging.error(f"JSON decode error in level configuration: {json_err}")
    except Exception as e:
        logging.error(f"Unexpected error loading level configuration: {e}")
    
    return default_level_config()

def default_level_config():
    """
    Returns a default level configuration if no specific level config is found.

    Returns:
        dict: Default configuration for the level.
    """
    logging.info("Using default level configuration.")
    return {
        'background': 'assets/background_default.png',
        'obstacle_speed': PIPE_SPEED,
        'obstacle_type': 'pipe',
        'num_obstacles': 3,
        'quantum_probability': 0.01,
        'quantum_element': 'QBlackHole',
        'gap_size': PIPE_GAP,
        'pipe_variants': PIPE_VARIANT_COLORS  # Use defined pipe colors
    }

def get_level_background(level_config):
    """
    Retrieves the background image path for the given level configuration.

    Args:
        level_config (dict): Configuration dictionary for the level.

    Returns:
        str: File path to the background image.
    """
    return level_config.get('background', 'assets/background_default.png')

def add_initial_obstacles(level_config):
    """
    Adds initial obstacles based on the level configuration.

    Args:
        level_config (dict): Configuration dictionary for the level.

    Returns:
        list: List of initial obstacles for the level.
    """
    obstacles = []
    num_obstacles = level_config.get('num_obstacles', 3)
    pipe_variants = level_config.get('pipe_variants', PIPE_VARIANT_COLORS)

    for i in range(num_obstacles):
        pipe = Pipe(
            x=i * 300 + WIDTH,
            speed=level_config.get('obstacle_speed', PIPE_SPEED),
            pipe_gap=level_config.get('gap_size', PIPE_GAP)
        )
        pipe.color = pipe_variants[i % len(pipe_variants)]  # Use color variants cyclically
        obstacles.append(pipe)
    logging.info(f"Added {num_obstacles} initial obstacles based on level configuration.")
    return obstacles

def add_obstacle(level_config, obstacles, screen_width):
    """
    Adds an obstacle to the game based on the level configuration.

    Args:
        level_config (dict): Configuration dictionary for the level.
        obstacles (list): List of existing obstacles.
        screen_width (int): Width of the screen to determine the placement of the new obstacle.
    """
    pipe = Pipe(
        x=screen_width,
        speed=level_config.get('obstacle_speed', PIPE_SPEED),
        pipe_gap=level_config.get('gap_size', PIPE_GAP)
    )
    pipe.color = random.choice(level_config.get('pipe_variants', PIPE_VARIANT_COLORS))
    obstacles.append(pipe)
    logging.info(f"New obstacle added at x={screen_width}.")

def spawn_quantum_element(level_config, screen_width, screen_height):
    """
    Spawns a quantum element based on the level configuration.

    Args:
        level_config (dict): Configuration dictionary for the level.
        screen_width (int): Width of the screen for positioning the quantum element.
        screen_height (int): Height of the screen for positioning the quantum element.

    Returns:
        dict: Quantum element data, or None if spawning is not required.
    """
    if random.random() < level_config.get('quantum_probability', 0.01):
        quantum_type = level_config.get('quantum_element', 'QBlackHole')
        quantum_element = {
            'type': quantum_type,
            'x_position': random.randint(50, screen_width - 50),
            'y_position': random.randint(50, screen_height - 50),
            'radius': BLACK_HOLE_RADIUS if quantum_type == 'QBlackHole' else AURORA_RADIUS,
            'color': (0, 0, 0) if quantum_type == 'QBlackHole' else (0, 255, 255)
        }
        logging.info(f"Quantum element {quantum_type} spawned at ({quantum_element['x_position']}, {quantum_element['y_position']}).")
        return quantum_element
    return None

def handle_level_progression(score, current_level, background, screen, obstacles, level_config):
    """
    Handles level progression based on the player's score.

    Args:
        score (int): Current score of the player.
        current_level (int): Current level number.
        background (ScrollingBackground): Scrolling background object.
        screen (pygame.Surface): Screen surface to display the game.
        obstacles (list): List of current obstacles.
        level_config (dict): Configuration dictionary for the level.

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

        # Adjust game parameters as needed (e.g., speed, spawn rate)
        settings.PIPE_SPEED = new_level_config.get('obstacle_speed', settings.PIPE_SPEED) + 0.5
        settings.PIPE_SPAWN_RATE_FRAMES = max(30, settings.PIPE_SPAWN_RATE_FRAMES - 20)
        logging.info(f"Updated game difficulty: Pipe Speed={settings.PIPE_SPEED}, Spawn Rate Frames={settings.PIPE_SPAWN_RATE_FRAMES}.")

        return current_level, background, new_level_config
    else:
        return current_level, background, level_config