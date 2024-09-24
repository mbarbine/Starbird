# modules/collisions.py

import pygame
import logging
from threading import Lock
from modules.settings import *

# Lock to ensure thread safety for bird attributes
bird_lock = Lock()

def check_collisions(bird, obstacles, quantum_elements):
    """
    Checks for collisions with obstacles and quantum elements.

    Args:
        bird (Bird): The bird object.
        obstacles (list): List of obstacle objects.
        quantum_elements (list): List of quantum element objects.

    Returns:
        bool: True if a collision is detected, False otherwise.
    """
    collision = False

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if hasattr(obstacle, 'rect') and bird.rect.colliderect(obstacle.rect):
            logging.info("Collision detected with obstacle.")
            collision = True
            break

    # Check for collisions with quantum elements
    if not collision:
        for element in quantum_elements:
            if hasattr(element, 'rect') and bird.rect.colliderect(element.rect):
                logging.info("Collision detected with quantum element.")
                collision = True
                break

    return collision

def handle_collision(bird, collision_sound):
    """
    Handles the collision event by updating the bird's status and playing a sound.

    Args:
        bird (Bird): The bird object.
        collision_sound (pygame.mixer.Sound): The collision sound to play.
    """
    with bird_lock:
        # Stop bird movement and play collision sound
        bird.is_flapping = False
        bird.velocity = 0
        collision_sound.play()

        # Decrement lives and check for game over condition
        if hasattr(bird, 'lives') and bird.lives > 0:
            bird.lives -= 1
            logging.info(f"Handled collision: Bird lost a life. Lives remaining: {bird.lives}")
            if bird.lives <= 0:
                logging.info("No lives remaining. Game Over.")
        else:
            logging.info("No lives remaining.")

