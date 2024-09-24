# modules/quantum_handler.py

import logging
from modules.quantum_elements.QBlackHole import QBlackHole
from modules.quantum_elements.q_aurorabor import AuroraBorealis

def handle_quantum_event(bird, quantum_element):
    """
    Handles the effects of a quantum element on the bird.

    Args:
        bird (Bird): The bird object.
        quantum_element (QuantumElement): The quantum element object.
    """
    try:
        if isinstance(quantum_element, QBlackHole):
            # Example effect: Pull the bird towards the black hole, reducing velocity
            logging.info("Quantum Event: QBlackHole affecting bird.")
            bird.velocity -= 1  # Adjust based on desired effect
            bird.apply_power_up('gravity_pull')  # Example power-up effect

        elif isinstance(quantum_element, AuroraBorealis):
            # Example effect: Enhance bird's abilities, increasing velocity
            logging.info("Quantum Event: Aurora Borealis affecting bird.")
            bird.velocity += 1  # Adjust based on desired effect
            bird.apply_power_up('speed_boost')  # Example power-up effect

        else:
            # Default effect if quantum element type is unknown
            logging.warning("Quantum Event: Unknown quantum element type.")
    except Exception as e:
        logging.error(f"Error handling quantum event: {e}")


def quantum_event_task(bird, quantum_element):
    """
    Task to handle quantum events in a separate thread.

    Args:
        bird (Bird): The bird object.
        quantum_element (QuantumElement): The quantum element object.
    """
    try:
        # Perform the quantum event, modifying the bird's state
        handle_quantum_event(bird, quantum_element)
        logging.debug(f"Quantum event {quantum_element} processed.")
    except Exception as e:
        logging.error(f"Error in quantum event task: {e}")
