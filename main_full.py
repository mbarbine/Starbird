# main.py

import pygame
import sys
import concurrent.futures
import logging
import random
import os
from threading import Lock

# Import necessary modules
from modules.bird import Bird
from modules.pipe import Pipe
from modules.holocron import Holocron
from modules.dark_side import dark_side_choice
from modules.jedi_training import jedi_training
from modules.death_star import death_star_battle
from modules.level_loader import (
    load_level,
    get_level_background,
    add_initial_obstacles,
    add_obstacle,
    spawn_quantum_element,
    handle_level_progression
)
from modules.story import star_wars_intro, get_story_text
from modules.text_effects import draw_text
from modules.backgrounds import ScrollingBackground
from modules.quantum_flap import apply_quantum_flap  # Using corrected function
from modules.sound_utils import load_sound, play_background_music
from modules.event_handler import handle_events, handle_game_mechanics
from modules.screen_utils import draw_hud, start_screen, game_over_screen, pause_game
from modules.collisions import check_collisions, handle_collision
from modules.game_utils import (
    init_game_window,
    load_game_font,
    update_obstacles_with_dt,
    draw_game_elements,
    update_score,
    load_high_scores,
    save_high_scores,
    get_player_name
)
from modules.settings import (
    STARTING_LEVEL,
    CONTROL_SETTINGS,
    EVENT_TIMERS,
    EVENT_COOLDOWNS,
    EVENT_FREQUENCY,
    COLORS,
    LIGHTSABER_LENGTH,
    SOUNDS,
    MUSIC_VOLUME,
    SFX_VOLUME,
    FULLSCREEN,
    WIDTH,
    HEIGHT,
    FONT_SIZE,
    WINDOW_TITLE,
    START_SCREEN_COLOR,
    GAME_OVER_COLOR,
    FLAP_SOUND,
    HIT_SOUND,
    SHIELD_SOUND,
    LASER_SOUND,
    BACKGROUND_MUSIC,
    CONTROL_DISPLAY_TIME,
    HIGH_SCORE_FILE,
    GRAVITY,
)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize a lock for thread safety when modifying bird attributes
bird_lock = Lock()


def check_holocron_collection(bird, holocron, quantum_elements):
    """Checks if the bird has collected a Holocron."""
    if holocron and holocron.collect(bird.rect):
        logging.info("Holocron collected.")
        bird.apply_power_up("shield")  # Example power-up
        quantum_elements.remove(holocron)  # Remove collected Holocron


def main():
    """Main function to run the game."""
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Game window setup
    screen = init_game_window()
    clock = pygame.time.Clock()

    # Initialize Scrolling Background
    background = ScrollingBackground()

    # Load game font
    font = load_game_font()

    # Display the Start Screen
    start_screen(screen, font)

    # Determine initial level and load corresponding story
    current_level = STARTING_LEVEL
    intro_story = get_story_text(current_level)  # Fetch story text for the starting level

    # Display the Star Wars-style intro with the fetched story text
    star_wars_intro(intro_story, screen)

    # Initialize game variables
    score = 0
    high_scores = load_high_scores()
    bird = Bird(WIDTH // 4, HEIGHT // 2)
    bird.image = pygame.transform.scale(bird.image, (50, 50))
    bird.rect = bird.image.get_rect()
    bird.rect.x = WIDTH // 4
    bird.rect.y = HEIGHT // 2
    bird.is_flapping = False
    bird.velocity = 0
    bird.power_ups = []  # Initialize power-ups list
    bird.current_ability = None
    bird.ability_cooldown = 0
    bird.ability_timer = 0
    bird.ability_duration = 0
    bird.ability_active = False
    bird.ability_start_time = 0
    bird.ability_end_time = 0
    bird.shield = False
    bird.lightsaber = False
    bird.lightsaber_length = LIGHTSABER_LENGTH
    bird.lightsaber_timer = 0
    bird.lightsaber_cooldown = 0
    bird.lightsaber_active = False
    bird.lightsaber_start_time = 0
    bird.lightsaber_end_time = 0 
    # Ensure Bird is initialized with position
    bird.lives = 3  # Initialize lives (you can set this in settings)

    # Load level configuration
    try:
        level_config = load_level(current_level)
    except Exception as e:
        logging.error(f"Failed to load level {current_level}: {e}")
        pygame.quit()
        sys.exit()

    # Initialize obstacles
    obstacles = add_initial_obstacles(level_config)

    # Initialize quantum elements
    quantum_elements = []

    # Initialize Holocron
    holocron = Holocron(WIDTH, HEIGHT)
    if holocron:
        quantum_elements.append(holocron)

    # Initialize thread pool executor for handling quantum events
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    # Get quantum probability from level config
    QUANTUM_PROBABILITY = level_config.get('quantum_probability', 0.01)  # Reduced frequency

    # Load sound effects
    flap_sound = load_sound(FLAP_SOUND)
    collision_sound = load_sound(HIT_SOUND)
    shield_sound = load_sound(SHIELD_SOUND)
    lightsaber_sound = load_sound(LASER_SOUND)

    # Set sound volumes
    if flap_sound:
        flap_sound.set_volume(SFX_VOLUME)
    if collision_sound:
        collision_sound.set_volume(SFX_VOLUME)
    if shield_sound:
        shield_sound.set_volume(SFX_VOLUME)
    if lightsaber_sound:
        lightsaber_sound.set_volume(SFX_VOLUME)

    # Play background music
    play_background_music()
    
    running = True

    # Initialize event timers
    event_timers = EVENT_TIMERS.copy()

    # Initialize control display timer
    control_display_timer = pygame.time.get_ticks()

    # Main game loop
    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds (assuming 60 FPS)

        # Handle events (input, etc.)
        running = handle_events(bird, screen, flap_sound, shield_sound, lightsaber_sound)

        # Update background
        background.update(dt)
        background.draw(screen)

        # Update bird
        bird.update_with_dt(dt)

        # Handle quantum elements
        if quantum_elements:
            for quantum_element in quantum_elements.copy():  # Use copy to avoid modification during iteration
                executor.submit(quantum_event_task, bird, quantum_element)

        # Quantum Elements Spawning Logic
        if len(quantum_elements) < 1 and random.random() < QUANTUM_PROBABILITY:  # Limit to 1 element max
            quantum_element = spawn_quantum_element(level_config, WIDTH, HEIGHT)
            if quantum_element:
                quantum_elements.append(quantum_element)
                logging.debug("Quantum element spawned.")

        # Update and draw obstacles
        update_obstacles_with_dt(level_config, obstacles, score, current_level, dt)
        draw_game_elements(screen, bird, obstacles, quantum_elements)

        # Handle game mechanics with cooldowns
        handle_game_mechanics(screen, bird, obstacles, quantum_elements, event_timers)

        # Decrement event timers
        for event in event_timers:
            if event_timers[event] > 0:
                event_timers[event] -= 1

        # Check collisions
        if check_collisions(bird, obstacles, quantum_elements):
            handle_collision(bird, collision_sound)
            update_leaderboard(score, high_scores)
            if bird.lives <= 0:
                game_over_screen(screen, font, score, high_scores)  # Display Game Over Screen
                running = False

        # Level progression
        current_level, background, level_config = handle_level_progression(
            score,
            current_level,
            background,
            screen,
            obstacles,
            level_config
        )

        # Update QUANTUM_PROBABILITY if a new level was loaded
        QUANTUM_PROBABILITY = level_config.get('quantum_probability', 0.01)  # Reduced frequency

        # Update score based on passed obstacles
        score = update_score(bird, obstacles, score)

        # Draw HUD
        draw_hud(screen, font, score, high_scores, bird, control_display_timer, current_level)

        # Update display
        pygame.display.flip()

        # Check if bird is off-screen
        if bird.rect.y > HEIGHT or bird.rect.y < 0:
            update_leaderboard(score, high_scores)
            game_over_screen(screen, font, score, high_scores)  # Display Game Over Screen
            running = False

    # Shut down executor and quit
    executor.shutdown(wait=True)
    pygame.quit()


def update_score(bird, obstacles, score):
    """Updates the score based on obstacles passed."""
    for obstacle in obstacles:
        if isinstance(obstacle, Pipe) and bird.rect.x > obstacle.rect.x + obstacle.rect.width and not obstacle.passed:
            score += 1
            obstacle.passed = True  # Mark obstacle as passed
            logging.info(f"Score updated: {score}")
    return score


def handle_game_mechanics(screen, bird, obstacles, quantum_elements, event_timers):
    """
    Handles game mechanics such as event triggering with cooldowns.
    """
    # Jedi Training Event
    if event_timers['jedi_training'] <= 0 and random.random() < EVENT_FREQUENCY['jedi_training']:
        success = jedi_training(screen)  # Pass only screen
        if success:
            bird.apply_power_up("shield")
            logging.info("Jedi Training succeeded: Shield activated.")
        else:
            with bird_lock:
                bird.velocity += GRAVITY * 1.5
            logging.info("Jedi Training failed: Bird velocity increased.")
        event_timers['jedi_training'] = EVENT_COOLDOWNS['jedi_training']

    # Dark Side Event
    if event_timers['dark_side'] <= 0 and random.random() < EVENT_FREQUENCY['dark_side']:
        if dark_side_choice(screen):  # Pass the screen argument
            for obstacle in obstacles:
                obstacle.speed += 1
            logging.info("Dark Side event triggered: Increased obstacle speed.")
        else:
            bird.apply_power_up("shield")
            logging.info("Dark Side event triggered: Shield activated.")
        event_timers['dark_side'] = EVENT_COOLDOWNS['dark_side']

    # Hyperspace Event
    if event_timers['hyperspace'] <= 0 and random.random() < EVENT_FREQUENCY['hyperspace']:
        new_x = random.randint(50, WIDTH - 50)
        new_y = random.randint(50, HEIGHT - 50)
        bird.rect.x = new_x
        bird.rect.y = new_y
        with bird_lock:
            bird.velocity = 0
        logging.info(f"Hyperspace jump: Bird teleported to ({new_x}, {new_y}).")
        event_timers['hyperspace'] = EVENT_COOLDOWNS['hyperspace']

    # Holocron Spawn Event
    if event_timers['holocron'] <= 0 and random.random() < EVENT_FREQUENCY['holocron_spawn_rate']:
        holocron = Holocron(WIDTH, HEIGHT)
        quantum_elements.append(holocron)
        logging.info("Holocron spawned.")
        event_timers['holocron'] = EVENT_COOLDOWNS['holocron']


def quantum_event_task(bird, quantum_element):
    """Handles quantum events in a separate thread."""
    try:
        handle_quantum_event(bird, quantum_element)
    except Exception as e:
        logging.error(f"Error in quantum event task: {e}")


def handle_quantum_event(bird, quantum_element):
    """
    Handles the interaction between the bird and a quantum element.
    """
    try:
        # Example: Apply a quantum flap effect
        with bird_lock:
            bird.velocity = apply_quantum_flap()  # Correct function call
        logging.debug("Quantum event handled successfully.")
    except Exception as e:
        logging.error(f"Error in handle_quantum_event: {e}")


def update_obstacles_with_dt(level_config, obstacles, score, current_level, dt):
    """Updates obstacle positions and spawns new obstacles as needed, considering delta time."""
    for obstacle in obstacles:
        if hasattr(obstacle, 'update_with_dt'):
            obstacle.update_with_dt(dt)
        elif hasattr(obstacle, 'update'):
            obstacle.update()
        else:
            logging.error(f"Obstacle {obstacle} does not have an 'update' or 'update_with_dt' method.")

    spawn_interval = level_config.get('pipe_spawn_rate_frames', PIPE_SPAWN_RATE_FRAMES)
    if score % spawn_interval == 0 and score != 0:
        add_obstacle(level_config, obstacles, WIDTH)
        logging.debug("New obstacle spawned.")


def draw_game_elements(screen, bird, obstacles, quantum_elements):
    """Draws all game elements on the screen."""
    bird.draw(screen)
    draw_obstacles(screen, obstacles)
    draw_quantum_elements(screen, quantum_elements)


def draw_obstacles(screen, obstacles):
    """Draws all obstacles on the screen."""
    for obstacle in obstacles:
        if hasattr(obstacle, 'draw'):
            obstacle.draw(screen)
        else:
            logging.error(f"Obstacle {obstacle} does not have a 'draw' method.")


def draw_quantum_elements(screen, quantum_elements):
    """Draws all quantum elements on the screen."""
    for element in quantum_elements:
        if hasattr(element, 'draw'):
            element.draw(screen)
        else:
            logging.error(f"Quantum element {element} does not have a 'draw' method.")


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
            if collision_sound:
                collision_sound.play()
            if bird.lives <= 0:
                logging.info("No lives remaining. Game Over.")
        else:
            logging.info("No lives remaining.")
            if collision_sound:
                collision_sound.play()


def draw_hud(screen, font, score, high_scores, bird, control_display_timer, current_level):
    """Draws the Heads-Up Display (HUD) on the screen."""
    draw_text(f"Score: {score}", font, COLORS['BLUE'], 10, 10, screen)
    draw_text(f"High Score: {high_scores['top_score']} by {high_scores['player']}", font, COLORS['RED'], 10, 50, screen)
    draw_text(f"Level: {current_level}", font, COLORS['GREEN'], 10, 90, screen)
    draw_text(f"Lives: {bird.lives}", font, COLORS['YELLOW'], 10, 130, screen)
    active_ability = bird.get_current_ability()
    if active_ability:
        draw_text(f"Ability: {active_ability}", font, COLORS['CYAN'], 10, 170, screen)
    # Display current velocity for debugging
    draw_text(f"Velocity: {bird.velocity:.2f}", font, COLORS['WHITE'], 10, 210, screen)
    if pygame.time.get_ticks() - control_display_timer < CONTROL_DISPLAY_TIME:
        draw_text("Space: Flap, S: Shield, L: Lightsaber, P: Pause", font, COLORS['WHITE'], 10, HEIGHT - 50, screen)


def update_leaderboard(score, high_scores):
    """Updates the leaderboard with the current score."""
    if score > high_scores['top_score']:
        high_scores['top_score'] = score
        high_scores['player'] = get_player_name()
        save_high_scores(high_scores)
        logging.info(f"New high score achieved: {score} by {high_scores['player']}")


if __name__ == "__main__":
    main()
