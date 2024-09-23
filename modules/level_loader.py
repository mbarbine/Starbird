# modules/level_loader.py

import importlib
import json
import os
import random
import logging
from modules.pipe import Pipe
from modules.settings import PIPE_WIDTH, GAP_SIZE, PIPE_SPEED, HEIGHT, WIDTH

def load_level(level_number):
    """
    Loads the configuration for the specified level.

    Args:
        level_number (int): The number of the level to load.

    Returns:
        dict: Configuration data for the specified level.

    Raises:
        FileNotFoundError: If the level configuration file is not found.
        KeyError: If the specified level does not exist in the configuration file.
        json.JSONDecodeError: If there is an error parsing the JSON file.
    """
    config_path = os.path.join(os.path.dirname(__file__), '../levels/level_config.json')
    
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Level configuration file not found at {config_path}. Please check the path.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON file at {config_path}: {e}")
    
    level_key = f"level{level_number}"
    
    try:
        return config[level_key]
    except KeyError:
        raise KeyError(f"Level {level_number} does not exist in the configuration file.")

def spawn_quantum_element(level_config, screen_width, screen_height):
    """
    Spawns a quantum element based on the level configuration.

    Args:
        level_config (dict): The configuration data for the level.
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.

    Returns:
        QuantumElement: A quantum element object or None if not specified.
    """
    quantum_element_type = level_config.get('quantum_element', None)

    if quantum_element_type:
        try:
            quantum_module = importlib.import_module(f'quantum_elements.{quantum_element_type}')
            return quantum_module.create_quantum_element(screen_width, screen_height)
        except ImportError as e:
            logging.error(f"Error loading quantum element module '{quantum_element_type}': {e}")
    
    return None

def handle_level_progression(score, current_level, background, screen, obstacles, level_config):
    """
    Handles level progression based on the score.

    Args:
        score (int): Current game score.
        current_level (int): Current level number.
        background (ScrollingBackground): Current background object.
        screen (pygame.Surface): Pygame screen surface.
        obstacles (list): List of current obstacles.
        level_config (dict): Current level configuration.

    Returns:
        tuple: (updated_level_number, updated_background, updated_level_config)
    """
    LEVEL_THRESHOLD = 100  # Example threshold, adjust as needed

    if score != 0 and score % LEVEL_THRESHOLD == 0:
        current_level += 1
        logging.info(f"Progressing to level {current_level}.")
        try:
            new_level_config = load_level(current_level)
        except Exception as e:
            logging.error(f"Failed to load level {current_level}: {e}")
            # Retain the existing level_config if loading fails
            return current_level, background, level_config
        
        new_obstacles = add_initial_obstacles(new_level_config, current_level)
        if new_obstacles:
            obstacles.extend(new_obstacles)
            logging.info(f"Added {len(new_obstacles)} new obstacles for level {current_level}.")
        
        # Update background based on new level
        new_background_path = get_level_background(new_level_config)
        if new_background_path:
            background.load_new_background(new_background_path)
            logging.info(f"Background updated for level {current_level}.")
    
        # Return the new level configuration
        return current_level, background, new_level_config
    else:
        # No level progression; retain the current level_config
        return current_level, background, level_config

def add_initial_obstacles(level_config, level_number):
    """
    Adds initial obstacles based on the current level configuration.

    Args:
        level_config (dict): Configuration data for the level.
        level_number (int): Current level number.

    Returns:
        list: List of obstacle objects.
    """
    obstacles = []
    obstacle_speed = level_config.get('obstacle_speed', 5)
    obstacle_type = level_config.get('obstacle_type', 'pipe')
    num_obstacles = level_config.get('num_obstacles', 3)

    for _ in range(num_obstacles):
        obstacles.append(Pipe(WIDTH, obstacle_speed, GAP_SIZE))
    
    return obstacles

def get_level_background(level_config):
    """
    Retrieves the background image path for the level.

    Args:
        level_config (dict): Configuration data for the level.

    Returns:
        str: Path to the background image.
    """
    return level_config.get('background', '../assets/background.png')
