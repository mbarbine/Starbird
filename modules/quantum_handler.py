# modules/quantum_handler.py

import logging
from modules.quantum_elements.QBlackHole import QBlackHole
from modules.quantum_elements.q_aurorabor import AuroraBorealis

def handle_quantum_event(bird, quantum_element, current_velocity):
    """
    Handles the effects of a quantum element on the bird.

    Args:
        bird (Bird): The bird object.
        quantum_element (QuantumElement): The quantum element object.
        current_velocity (float): The bird's current velocity.

    Returns:
        float: The updated velocity after applying the quantum event.
    """
    if isinstance(quantum_element, QBlackHole):
        # Example effect: Pull the bird towards the black hole, reducing velocity
        logging.info("Quantum Event: QBlackHole affecting bird.")
        return current_velocity - 1  # Adjust based on desired effect
    elif isinstance(quantum_element, AuroraBorealis):
        # Example effect: Enhance bird's abilities, increasing velocity
        logging.info("Quantum Event: Aurora Borealis affecting bird.")
        return current_velocity + 1  # Adjust based on desired effect
    else:
        # Default effect if quantum element type is unknown
        logging.warning("Quantum Event: Unknown quantum element type.")
        return current_velocity
