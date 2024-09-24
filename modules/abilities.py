# modules/abilities.py

import logging
from modules.force_lightning import activate_force_lightning

def activate_special_ability(bird):
    """Activates the bird's special ability based on current ability type."""
    ability = bird.get_current_ability()
    logging.info(f"Activating special ability: {ability}")
    if ability == 'Shield':
        bird.apply_power_up("shield")
    elif ability == 'Laser':
        activate_force_lightning(bird.rect)
    elif ability == 'Speed':
        bird.speed_boost()
    else:
        logging.warning(f"Unknown ability: {ability}")

def quantum_event_task(bird, quantum_element):
    """Handles quantum events in a separate thread."""
    try:
        from modules.event_handler import handle_quantum_event
        handle_quantum_event(bird, quantum_element)
    except Exception as e:
        logging.error(f"Error in quantum event task: {e}")
