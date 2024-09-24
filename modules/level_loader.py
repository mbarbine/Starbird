# modules/level_loader.py

import json
import logging
from modules.settings import PIPE_SPEED, PIPE_GAP, BLACK_HOLE_RADIUS, AURORA_RADIUS

def load_level_config(level_number):
    """
    Loads level configuration from the JSON file.

    Args:
        level_number (int): The current level number.

    Returns:
        dict: Level configuration dictionary.
    """
    try:
        with open('levels/level_config.json') as f:
            config = json.load(f)
            level_key = f'level{level_number}'
            if level_key in config:
                level_config = config[level_key]
                logging.info(f"Level {level_number} configuration loaded.")
                return level_config
            else:
                logging.warning(f"Level {level_number} configuration not found. Using default settings.")
                return default_level_config()
    except Exception as e:
        logging.error(f"Error loading level configuration: {e}")
        return default_level_config()

def default_level_config():
    """Returns a default level configuration."""
    return {
        'background': 'assets/background_default.png',
        'obstacle_speed': PIPE_SPEED,
        'obstacle_type': 'pipe',
        'num_obstacles': 3,
        'quantum_probability': 0.01,
        'quantum_element': 'QBlackHole',
        'gap_size': PIPE_GAP
    }
