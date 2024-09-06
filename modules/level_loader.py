import importlib
import json
import os
from settings import *
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

def get_level_background(level_config):
    """
    Dynamically imports and returns the background module for the given level.

    Args:
        level_config (dict): The configuration data for the level.

    Returns:
        module: The background module for the level.
    """
    background_module_name = level_config.get('background_module', 'default_background')
    try:
        background_module = importlib.import_module(f'backgrounds.{background_module_name}')
        return background_module
    except ImportError as e:
        print(f"Error loading background module '{background_module_name}': {e}")
        return importlib.import_module('backgrounds.default_background')

def get_obstacle_speed(level_config):
    """
    Retrieves the obstacle speed for the given level.

    Args:
        level_config (dict): The configuration data for the level.

    Returns:
        int: The speed of the obstacles.
    """
    return level_config.get('obstacle_speed', 5)  # Default speed is 5 if not specified

def add_obstacle(level_config, obstacle_list, screen_width):
    """
    Adds an obstacle to the obstacle list based on the level configuration.

    Args:
        level_config (dict): The configuration data for the level.
        obstacle_list (list): The current list of obstacles.
        screen_width (int): The width of the screen.

    Returns:
        list: Updated list of obstacles.
    """
    obstacle_type = level_config.get('obstacle_type', 'pipe')
    obstacle_position = screen_width + 200  # Example of placing an obstacle off-screen to the right

    # Example obstacle import and addition
    try:
        obstacle_module = importlib.import_module(f'obstacles.{obstacle_type}')
        new_obstacle = obstacle_module.create_obstacle(obstacle_position)
        obstacle_list.append(new_obstacle)
    except ImportError as e:
        print(f"Error loading obstacle module '{obstacle_type}': {e}")

    return obstacle_list

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
            print(f"Error loading quantum element module '{quantum_element_type}': {e}")
    
    return None
