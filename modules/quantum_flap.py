# modules/quantum_flap.py

import random
from modules.settings import QUANTUM_FLAP_STRENGTH, QUANTUM_FLAP_SCALING_FACTOR, QUANTUM_FLAP_VARIANTS, QUANTUM_FLAP_PROBABILITY

def apply_quantum_flap(bird_velocity, event_type='standard'):
    """
    Applies a quantum flap effect to the bird's velocity based on event type.

    Args:
        bird_velocity (float): The current velocity of the bird.
        event_type (str): Type of quantum event ('standard', 'boost', 'reduced').

    Returns:
        float: The updated velocity after applying the quantum flap.
    """
    # Determine flap strength based on event type
    flap_strength = QUANTUM_FLAP_VARIANTS.get(event_type, QUANTUM_FLAP_STRENGTH)
    
    # Apply the scaling factor to the flap strength
    scaled_flap_strength = flap_strength * QUANTUM_FLAP_SCALING_FACTOR

    # Return the updated velocity
    return bird_velocity + scaled_flap_strength

def random_quantum_flap(bird_velocity):
    """
    Applies a random quantum flap effect based on probability.

    Args:
        bird_velocity (float): The current velocity of the bird.

    Returns:
        float: The updated velocity after applying a random quantum flap.
    """
    if random.random() < QUANTUM_FLAP_PROBABILITY:
        # Choose a random event type
        event_type = random.choice(list(QUANTUM_FLAP_VARIANTS.keys()))
        return apply_quantum_flap(bird_velocity, event_type)
    return bird_velocity
