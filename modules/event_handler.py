# modules/event_handler.py

import pygame
import sys
import logging
import random
from threading import Lock
import modules.settings as settings
from modules.quantum_flap import apply_quantum_flap
from modules.jedi_training import jedi_training
from modules.dark_side import dark_side_choice
from modules.holocron import Holocron
from modules.screen_utils import pause_game
from modules.game_utils import check_event_timers, update_event_timers, reset_bird_position

# Lock for thread safety when accessing bird attributes
bird_lock = Lock()

def handle_events(bird, screen, sound_effects, font, dt):
    """
    Handles user inputs and events during the game.

    Args:
        bird (Bird): The bird object controlled by the player.
        screen (pygame.Surface): The game screen.
        sound_effects (dict): Dictionary of sound effects.
        font (pygame.font.Font): The font used for displaying text.
        dt (float): Delta time for frame consistency.

    Returns:
        bool: True if the game should continue running, False to exit.
    """
    keys = pygame.key.get_pressed()

    # Handle continuous flapping when the flap key is held down
    if keys[settings.CONTROL_SETTINGS['flap_key']]:
        trigger_flap(bird, sound_effects)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == pygame.KEYDOWN:
            handle_keydown_events(event, bird, screen, sound_effects, font)

    return True

def trigger_flap(bird, sound_effects):
    """Triggers bird flap and plays sound effect."""
    if not bird.is_flapping and bird.flap_cooldown <= 0:
        bird.flap()
        play_sound(sound_effects, 'flap')
        logging.debug("Bird flapped.")

def handle_keydown_events(event, bird, screen, sound_effects, font):
    """Handles keydown events for the game."""
    if event.key == settings.CONTROL_SETTINGS['pause_key']:
        logging.info("Pause key pressed. Pausing game.")
        pause_game(screen, font)
    elif event.key == settings.CONTROL_SETTINGS['shield_key']:
        activate_power_up(bird, 'shield', sound_effects, "Shield activated.")
    elif event.key == settings.CONTROL_SETTINGS['lightsaber_key']:
        activate_power_up(bird, 'lightsaber', sound_effects, "Lightsaber activated.")
    elif event.key == settings.CONTROL_SETTINGS['quit_key']:
        quit_game()

def activate_power_up(bird, power_up_type, sound_effects, log_message):
    """Activates a power-up for the bird if conditions are met."""
    if not getattr(bird, f"{power_up_type}_active") and getattr(bird, f"{power_up_type}_duration") <= 0:
        bird.apply_power_up(power_up_type)
        play_sound(sound_effects, power_up_type)
        logging.info(log_message)

def play_sound(sound_effects, effect_name):
    """Plays a sound effect if available."""
    if effect_name in sound_effects:
        sound_effects[effect_name].play()

def quit_game():
    """Handles the game quitting process."""
    logging.info("Quit event detected. Exiting game.")
    pygame.quit()
    sys.exit()

def handle_quantum_event(bird, quantum_element):
    """
    Handles interaction between the bird and a quantum element.

    Args:
        bird (Bird): The bird object.
        quantum_element: The quantum element affecting the bird.
    """
    try:
        with bird_lock:
            bird.velocity = apply_quantum_flap()
        logging.debug("Quantum event handled successfully.")
    except Exception as e:
        logging.error(f"Error in handle_quantum_event: {e}")

def handle_game_mechanics(screen, bird, obstacles, quantum_elements, event_timers, current_time):
    """
    Manages game mechanics, including random events and cooldowns.

    Args:
        screen (pygame.Surface): The game screen.
        bird (Bird): The bird object.
        obstacles (list): List of obstacle objects.
        quantum_elements (list): List of quantum elements.
        event_timers (dict): Dictionary of event timers for cooldowns.
        current_time (float): The current game time in seconds.
    """
    # Update event timers
    update_event_timers(event_timers, current_time)

    # Handle Jedi Training Event
    if check_event_timers(event_timers, 'jedi_training'):
        trigger_jedi_training(screen, bird, event_timers)

    # Handle Dark Side Event
    if check_event_timers(event_timers, 'dark_side'):
        trigger_dark_side(screen, bird, obstacles, event_timers)

    # Handle Hyperspace Event
    if check_event_timers(event_timers, 'hyperspace'):
        trigger_hyperspace_jump(bird, event_timers)

    # Handle Holocron Spawn Event
    if check_event_timers(event_timers, 'holocron'):
        spawn_holocron(settings.WIDTH, settings.HEIGHT, quantum_elements, event_timers)

def trigger_jedi_training(screen, bird, event_timers):
    """Triggers the Jedi Training event."""
    success = jedi_training(screen)
    if success:
        bird.apply_power_up("shield")
        logging.info("Jedi Training succeeded: Shield activated.")
    else:
        increase_bird_velocity(bird)
    event_timers['jedi_training'] = settings.EVENT_COOLDOWNS['jedi_training']

def trigger_dark_side(screen, bird, obstacles, event_timers):
    """Triggers the Dark Side event."""
    if dark_side_choice(screen):
        for obstacle in obstacles:
            obstacle.speed += 1
        logging.info("Dark Side event triggered: Increased obstacle speed.")
    else:
        bird.apply_power_up("shield")
        logging.info("Dark Side event triggered: Shield activated.")
    event_timers['dark_side'] = settings.EVENT_COOLDOWNS['dark_side']

def trigger_hyperspace_jump(bird, event_timers):
    """Triggers the Hyperspace jump event."""
    new_x = random.randint(50, settings.WIDTH - 50)
    new_y = random.randint(50, settings.HEIGHT - 50)
    reset_bird_position(bird, new_x, new_y)
    logging.info(f"Hyperspace jump: Bird teleported to ({new_x}, {new_y}).")
    event_timers['hyperspace'] = settings.EVENT_COOLDOWNS['hyperspace']

def spawn_holocron(width, height, quantum_elements, event_timers):
    """Spawns a Holocron on the game screen."""
    holocron = Holocron(width, height)
    quantum_elements.append(holocron)
    logging.info("Holocron spawned.")
    event_timers['holocron'] = settings.EVENT_COOLDOWNS['holocron']

def increase_bird_velocity(bird):
    """Increases the bird's velocity as a penalty."""
    with bird_lock:
        bird.velocity += settings.GRAVITY * 1.5
    logging.info("Jedi Training failed: Bird velocity increased.")

def check_collisions(bird, obstacles, quantum_elements):
    """
    Checks for collisions between the bird and obstacles or quantum elements.

    Args:
        bird (Bird): The bird object.
        obstacles (list): List of obstacles in the game.
        quantum_elements (list): List of quantum elements.

    Returns:
        bool: True if a collision is detected, False otherwise.
    """
    if check_bird_collisions(bird, obstacles) or check_bird_collisions(bird, quantum_elements):
        logging.info("Collision detected.")
        return True
    return False

def check_bird_collisions(bird, elements):
    """Checks for collisions between the bird and a list of elements."""
    for element in elements:
        if hasattr(element, 'rect') and bird.rect.colliderect(element.rect):
            return True
    return False

def handle_collision(bird, collision_sound):
    """
    Handles the collision event by stopping the bird and playing a sound.

    Args:
        bird (Bird): The bird object.
        collision_sound (pygame.mixer.Sound): The collision sound effect.
    """
    with bird_lock:
        bird.is_flapping = False
        bird.velocity = 0
        collision_sound.play()
        update_bird_lives(bird)

def update_bird_lives(bird):
    """Updates the bird's lives after a collision."""
    if hasattr(bird, 'lives') and bird.lives > 0:
        bird.lives -= 1
        logging.info(f"Handled collision: Bird lost a life. Lives remaining: {bird.lives}")
        if bird.lives <= 0:
            logging.info("No lives remaining. Game Over.")
    else:
        logging.info("No lives remaining.")
