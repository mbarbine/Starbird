# modules/event_handler.py

import pygame
import random
import logging
from threading import Lock
import modules.settings as settings
from modules.quantum_flap import apply_quantum_flap

bird_lock = Lock()  # Lock for thread safety

def handle_events(bird, screen, flap_sound, shield_sound, lightsaber_sound, font, dt):
    """Handles user input and events."""
    keys = pygame.key.get_pressed()
    
    # Handle continuous flapping
    if keys[settings.CONTROL_SETTINGS['flap_key']]:
        if not bird.is_flapping and bird.flap_cooldown <= 0:
            bird.flap()
            flap_sound.play()  # Play flap sound

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            logging.info("Quit event detected.")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == settings.CONTROL_SETTINGS['pause_key']:
                logging.info("Pause key pressed. Pausing game.")
                from modules.screens import pause_game
                pause_game(screen, font)
            elif event.key == settings.CONTROL_SETTINGS['shield_key']:
                if not bird.shield_active and bird.shield_duration <= 0:
                    bird.apply_power_up("shield")
                    shield_sound.play()  # Play shield activation sound
                    logging.info("Shield key pressed. Shield activated.")
            elif event.key == settings.CONTROL_SETTINGS['lightsaber_key']:
                if not bird.lightsaber_active:
                    bird.apply_power_up("lightsaber")
                    lightsaber_sound.play()  # Play lightsaber sound
                    logging.info("Lightsaber key pressed. Lightsaber activated.")
    return True  # Continue running

def handle_quantum_event(bird, quantum_element):
    """Handles the interaction between the bird and a quantum element."""
    try:
        # Use apply_quantum_flap to modify velocity with quantum effect
        with bird_lock:
            bird.velocity = apply_quantum_flap()  # Correct function call
        logging.debug("Quantum event handled successfully.")
    except Exception as e:
        logging.error(f"Error in handle_quantum_event: {e}")

def handle_game_mechanics(screen, bird, obstacles, quantum_elements, event_timers):
    """Handles game mechanics such as event triggering with cooldowns."""
    # Jedi Training Event
    from modules.jedi_training import jedi_training
    if event_timers['jedi_training'] <= 0 and random.random() < settings.EVENT_FREQUENCY['jedi_training']:
        success = jedi_training(screen)  # Pass only screen
        if success:
            bird.apply_power_up("shield")
            logging.info("Jedi Training succeeded: Shield activated.")
        else:
            with bird_lock:
                bird.velocity += settings.GRAVITY * 1.5
            logging.info("Jedi Training failed: Bird velocity increased.")
        event_timers['jedi_training'] = settings.EVENT_COOLDOWNS['jedi_training']

    # Dark Side Event
    from modules.dark_side import dark_side_choice
    if event_timers['dark_side'] <= 0 and random.random() < settings.EVENT_FREQUENCY['dark_side']:
        if dark_side_choice(screen):  # Pass the screen argument
            for obstacle in obstacles:
                obstacle.speed += 1
            logging.info("Dark Side event triggered: Increased obstacle speed.")
        else:
            bird.apply_power_up("shield")
            logging.info("Dark Side event triggered: Shield activated.")
        event_timers['dark_side'] = settings.EVENT_COOLDOWNS['dark_side']

    # Hyperspace Event
    if event_timers['hyperspace'] <= 0 and random.random() < settings.EVENT_FREQUENCY['hyperspace']:
        new_x = random.randint(50, settings.WIDTH - 50)
        new_y = random.randint(50, settings.HEIGHT - 50)
        bird.rect.x = new_x
        bird.rect.y = new_y
        with bird_lock:
            bird.velocity = 0
        logging.info(f"Hyperspace jump: Bird teleported to ({new_x}, {new_y}).")
        event_timers['hyperspace'] = settings.EVENT_COOLDOWNS['hyperspace']

    # Holocron Spawn Event
    from modules.holocron import Holocron
    if event_timers['holocron'] <= 0 and random.random() < settings.EVENT_FREQUENCY['holocron_spawn_rate']:
        holocron = Holocron(settings.WIDTH, settings.HEIGHT)
        quantum_elements.append(holocron)
        logging.info("Holocron spawned.")
        event_timers['holocron'] = settings.EVENT_COOLDOWNS['holocron']

def check_collisions(bird, obstacles, quantum_elements):
    """Checks for collisions with obstacles and quantum elements."""
    collision = False
    for obstacle in obstacles:
        if hasattr(obstacle, 'rect') and bird.rect.colliderect(obstacle.rect):
            logging.info("Collision detected with obstacle.")
            collision = True
            break
    if not collision:
        for element in quantum_elements:
            if hasattr(element, 'rect') and bird.rect.colliderect(element.rect):
                logging.info("Collision detected with quantum element.")
                collision = True
                break
    return collision

def handle_collision(bird, collision_sound):
    """Handles the collision event."""
    with bird_lock:
        bird.is_flapping = False
        bird.velocity = 0
        if hasattr(bird, 'lives') and bird.lives > 0:
            bird.lives -= 1
            logging.info(f"Handled collision: Bird lost a life. Lives remaining: {bird.lives}")
            collision_sound.play()
            if bird.lives <= 0:
                logging.info("No lives remaining. Game Over.")
        else:
            logging.info("No lives remaining.")
            collision_sound.play()
