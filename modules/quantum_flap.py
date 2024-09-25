# modules/quantum_flap.py

import random
import numpy as np
import logging
from modules.settings import (
    QUANTUM_FLAP_STRENGTH,
    QUANTUM_FLAP_SCALING_FACTOR,
    QUANTUM_FLAP_VARIANTS,
    QUANTUM_FLAP_PROBABILITY,
    QUANTUM_FLAP_COOLDOWN_TIME
)

# Initialize the last event time to ensure cooldown between events
last_quantum_flap_time = 0

def apply_quantum_flap(bird, event_type='standard'):
    """
    Applies a quantum flap effect to the bird's velocity based on event type.

    Args:
        bird (Bird): The bird object to which the quantum flap is applied.
        event_type (str): Type of quantum event ('standard', 'boost', 'reduced').

    Returns:
        None
    """
    # Isolate complex calculation in a separate function
    scaled_flap_strength = calculate_scaled_flap_strength(event_type)
    
    # Update bird's velocity using numpy to ensure numerical stability
    bird.velocity = np.clip(bird.velocity + scaled_flap_strength, bird.min_velocity, bird.max_velocity)
    logging.info(f"Quantum flap applied. New bird velocity: {bird.velocity}.")

def calculate_scaled_flap_strength(event_type):
    """
    Calculates the scaled flap strength based on event type.

    Args:
        event_type (str): Type of quantum event ('standard', 'boost', 'reduced').

    Returns:
        float: The calculated scaled flap strength.
    """
    # Determine flap strength based on event type
    flap_strength = QUANTUM_FLAP_VARIANTS.get(event_type, QUANTUM_FLAP_STRENGTH)
    
    # Apply the scaling factor to the flap strength
    scaled_flap_strength = flap_strength * QUANTUM_FLAP_SCALING_FACTOR
    logging.debug(f"Quantum flap event: {event_type}, base strength: {flap_strength}, scaled strength: {scaled_flap_strength}.")
    
    return scaled_flap_strength

def random_quantum_flap(bird, current_time):
    """
    Applies a random quantum flap effect based on probability and cooldown.

    Args:
        bird (Bird): The bird object to which the random quantum flap is applied.
        current_time (float): The current game time in seconds.

    Returns:
        None
    """
    global last_quantum_flap_time
    
    # Check if enough time has passed since the last quantum flap event
    if (current_time - last_quantum_flap_time) > QUANTUM_FLAP_COOLDOWN_TIME:
        if random.random() < QUANTUM_FLAP_PROBABILITY:
            # Choose a random event type
            event_type = random.choice(list(QUANTUM_FLAP_VARIANTS.keys()))
            logging.info(f"Random quantum event triggered: {event_type}")
            apply_quantum_flap(bird, event_type)
            last_quantum_flap_time = current_time
        else:
            logging.debug("No quantum event triggered.")
    else:
        logging.debug(f"Quantum flap cooldown active. Time remaining: {QUANTUM_FLAP_COOLDOWN_TIME - (current_time - last_quantum_flap_time):.2f} seconds.")
