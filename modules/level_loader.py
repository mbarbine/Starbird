# modules/level_loader.py

import json
import logging
import os
import random
from modules.settings import (
    WIDTH, HEIGHT, PIPE_SPEED, PIPE_GAP, BLACK_HOLE_RADIUS, AURORA_RADIUS,
    LEVEL_THRESHOLD, PIPE_SPAWN_RATE_FRAMES, PIPE_VARIANT_COLORS
)
from modules.pipe import Pipe
from modules.holocron import Holocron
from modules.backgrounds import ScrollingBackground

# Level Configuration Dictionary for hard-coded levels
LEVEL_CONFIGS = {
    1: {
        'background': 'assets/background_level1.png',
        'pipe_speed': 5,
        'pipe_spawn_rate_frames': 90,
        'num_obstacles': 3,
        'quantum_probability': 0.1,
        'quantum_element': 'QBlackHole',
        'gap_size': 180,
        'pipe_variants': [(34, 139, 34), (107, 142, 35), (154, 205, 50)]
    },
    2: {
        'background': 'assets/background_level2.png',
        'pipe_speed': 6,
        'pipe_spawn_rate_frames': 80,
        'num_obstacles': 4,
        'quantum_probability': 0.015,
        'quantum_element': 'AuroraBorealis',
        'gap_size': 160,
        'pipe_variants': [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    },
    # Additional hard-coded levels can be added here
}

def load_level(level_number):
    """
    Loads the level configuration based on the level number, either from the predefined
    dictionary or from an external JSON file.

    Args:
        level_number (int): The current level number.

    Returns:
        dict: Level configuration settings.
    """
    level_file_path = os.path.join('levels', 'level_config.json')

    if os.path.exists(level_file_path):
        # Load level from JSON file if available
        try:
            with open(level_file_path, 'r') as file:
                level_data = json.load(file)
                level_key = f'level{level_number}'
                if level_key in level_data:
                    level_config = level_data[level_key]
                    logging.info(f"Level {level_number} configuration loaded successfully from JSON.")
                    return level_config
                else:
                    logging.warning(f"Level {level_number} configuration not found in JSON. Using predefined settings.")
                    return LEVEL_CONFIGS.get(level_number, default_level_config())
        except json.JSONDecodeError as json_err:
            logging.error(f"JSON decode error in level configuration: {json_err}")
        except Exception as e:
            logging.error(f"Unexpected error loading level configuration: {e}")
    else:
        # Fall back to predefined dictionary if JSON file doesn't exist
        if level_number in LEVEL_CONFIGS:
            logging.info(f"Level {level_number} loaded from predefined configuration.")
            return LEVEL_CONFIGS[level_number]
        else:
            logging.warning(f"Level {level_number} not found. Loading default level configuration.")
            return default_level_config()

    # If JSON loading fails, return default configuration
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
        'pipe_speed': PIPE_SPEED,
        'pipe_spawn_rate_frames': 100,
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
            speed=level_config.get('pipe_speed', PIPE_SPEED),
            pipe_gap=level_config.get('gap_size', PIPE_GAP)
        )
        pipe.color = pipe_variants[i % len(pipe_variants)]  # Use color variants cyclically
        obstacles.append(pipe)
    logging.info(f"Added {num_obstacles} initial obstacles based on level configuration.")
    return obstacles

def add_obstacle(level_config, obstacles, screen_width):
    """
    Adds a new obstacle to the game based on the level configuration.

    Args:
        level_config (dict): Configuration dictionary for the level.
        obstacles (list): List of existing obstacles.
        screen_width (int): Width of the screen to determine the placement of the new obstacle.
    """
    pipe = Pipe(
        x=screen_width,
        speed=level_config.get('pipe_speed', PIPE_SPEED),
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
        QuantumElement or None: The spawned quantum element or None if not spawned.
    """
    if random.random() < level_config.get('quantum_probability', 0.01):
        quantum_type = level_config.get('quantum_element', 'QBlackHole')
        if quantum_type == 'QBlackHole':
            radius = BLACK_HOLE_RADIUS
            color = settings.COLORS.get('BLACK', (0, 0, 0))
        elif quantum_type == 'AuroraBorealis':
            radius = AURORA_RADIUS
            color = settings.COLORS.get('CYAN', (0, 255, 255))
        else:
            radius = BLACK_HOLE_RADIUS
            color = settings.COLORS.get('BLACK', (0, 0, 0))
        
        x = random.randint(radius, screen_width - radius)
        y = random.randint(radius, screen_height - radius)
        rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        quantum_element = QuantumElement(rect, quantum_type)
        logging.info(f"Quantum element {quantum_type} spawned at ({x}, {y}).")
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
        global PIPE_SPEED, PIPE_SPAWN_RATE_FRAMES  # Declare as global to modify
        PIPE_SPEED = new_level_config.get('pipe_speed', PIPE_SPEED) + 0.5
        PIPE_SPAWN_RATE_FRAMES = max(60, PIPE_SPAWN_RATE_FRAMES - 10)
        logging.info(f"Updated game difficulty: Pipe Speed={PIPE_SPEED}, Spawn Rate Frames={PIPE_SPAWN_RATE_FRAMES}.")

        return current_level, background, new_level_config
    else:
        return current_level, background, level_config
