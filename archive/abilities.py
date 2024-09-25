# modules/abilities.py

import logging
from modules.force_lightning import activate_force_lightning
from threading import Lock

# Lock for thread safety when altering bird's abilities
ability_lock = Lock()

def activate_special_ability(bird):
    """
    Activates the bird's special ability based on its current ability type.

    Args:
        bird (Bird): The bird object whose ability is to be activated.
    """
    with ability_lock:  # Ensure thread safety when modifying the bird's attributes
        ability = bird.get_current_ability()
        logging.info(f"Activating special ability: {ability}")

        if ability == 'Shield':
            bird.apply_power_up("shield")
            logging.info("Shield ability activated.")
        elif ability == 'Laser':
            activate_force_lightning(bird.rect)
            logging.info("Laser ability activated.")
        elif ability == 'Speed':
            bird.speed_boost()
            logging.info("Speed boost ability activated.")
        elif ability == 'Invisibility':
            bird.become_invisible()
            logging.info("Invisibility ability activated.")
        elif ability == 'Quantum Flap':
            bird.quantum_flap()
            logging.info("Quantum Flap ability activated.")
        else:
            logging.warning(f"Unknown ability: {ability}")

def quantum_event_task(bird, quantum_element):
    """
    Handles quantum events in a separate thread. Applies quantum effects on the bird.

    Args:
        bird (Bird): The bird object to apply quantum effects to.
        quantum_element (dict): Details of the quantum element (e.g., type, position).

    This function is run in a separate thread to avoid blocking the main game loop.
    """
    try:
        # Import here to avoid circular dependency issues
        from modules.event_handler import handle_quantum_event

        logging.info(f"Handling quantum event: {quantum_element['type']} at ({quantum_element['x_position']}, {quantum_element['y_position']})")
        
        handle_quantum_event(bird, quantum_element)
        logging.info(f"Quantum event {quantum_element['type']} handled successfully.")
    except KeyError as ke:
        logging.error(f"KeyError in quantum event task: {ke} - Missing expected key in quantum_element.")
    except Exception as e:
        logging.error(f"Error in quantum event task: {e}")

# Additional ability methods can be added here if needed

# Example additional methods (to be implemented in Bird class or elsewhere):
# def bird.become_invisible():
#     """
#     Makes the bird temporarily invisible, avoiding obstacles.
#     """
#     # Implement invisibility logic
#     pass

# def bird.quantum_flap():
#     """
#     Enhances the bird's flap with quantum effects for a short period.
#     """
#     # Implement quantum flap logic
#     pass

# def bird.speed_boost():
#     """
#     Temporarily increases the bird's speed for rapid movement.
#     """
#     # Implement speed boost logic
#     pass
# abilities.py
import logging

class Abilities:
    def __init__(self, bird):
        self.bird = bird

    def apply_power_up(self, power_up_type):
        if power_up_type == "shield":
            self.bird.activate_shield()
        elif power_up_type == "lightsaber":
            self.bird.activate_lightsaber()
        elif power_up_type == "shrink":
            self.bird.shrink()
        else:
            logging.warning(f"Unknown power-up type: {power_up_type}")

    def reset_abilities(self):
        self.bird.deactivate_all()
# abilities.py
import logging

class Abilities:
    def __init__(self, bird):
        self.bird = bird

    def apply_power_up(self, power_up_type):
        """
        Applies a specific power-up to the bird.

        Args:
            power_up_type (str): The type of power-up to apply.
        """
        if power_up_type == "shield":
            self.bird.activate_shield()
        elif power_up_type == "lightsaber":
            self.bird.activate_lightsaber()
        elif power_up_type == "shrink":
            self.bird.shrink()
        else:
            logging.warning(f"Unknown power-up type: {power_up_type}")

    def reset_abilities(self):
        """Resets all abilities to their default state."""
        self.bird.deactivate_all()
