# main.py

import pygame
import sys
import logging
import random
import concurrent.futures
from threading import Lock

from modules.bird import Bird
from modules.pipe import Pipe
import modules.settings as settings
from modules.force_lightning import activate_force_lightning
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
from modules.story import load_story, display_level_story
from modules.text_effects import draw_text
from modules.backgrounds import ScrollingBackground
from modules.quantum_flap import apply_quantum_flap, random_quantum_flap
from modules.sound_utils import (
    load_sound,
    play_background_music,
    stop_background_music
)
from modules.sound_effects import (
    load_sound_effect,
    play_sound_effect
)
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

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize a lock for thread safety when modifying bird attributes
bird_lock = Lock()

def main():
    """Main function to run the game."""
    pygame.init()
    pygame.mixer.init()

    # Game window setup
    screen = init_game_window()
    clock = pygame.time.Clock()

    # Load sound effects using sound_effects.py
    sound_effects = {
        'flap': load_sound_effect('flap.wav'),
        'collision': load_sound_effect('hit.wav'),
        'shield': load_sound_effect('shield.wav'),
        'laser': load_sound_effect('laser.wav')
    }

    # DEBUG: Print the loaded sound_effects keys
    logging.info(f"Loaded sound effects keys: {list(sound_effects.keys())}")

    # Start playing background music
    play_background_music()

    # Initialize scrolling background
    background = ScrollingBackground('background_default.png', speed=2)

    # Load game font
    font = load_game_font()

    # Display the start screen
    start_screen(screen, font)

    # Load story and display intro
    story_dict = load_story()
    intro_text = story_dict.get("# Intro", "Welcome to the Game!\nPress SPACE or ENTER to continue.")
    star_wars_intro(screen, font, intro_text, sound_effects)

    # Initialize game variables
    current_level = settings.STARTING_LEVEL
    score = 0
    high_scores = load_high_scores()
    bird = Bird(x=settings.BIRD_START_X, y=settings.BIRD_START_Y)
    bird.lives = settings.BIRD_MAX_LIVES  # Initialize lives

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

    # Initialize Holocron if applicable
    holocron = Holocron(settings.WIDTH, settings.HEIGHT)
    if holocron:
        quantum_elements.append(holocron)

    # Initialize thread pool executor for handling quantum events
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    # Get quantum probability from level config
    QUANTUM_PROBABILITY = level_config.get('quantum_probability', 0.01)

    running = True

    # Initialize event timers
    event_timers = settings.EVENT_TIMERS.copy()

    # Initialize control display timer
    control_display_timer = pygame.time.get_ticks()

    # Main game loop
    while running:
        dt = clock.tick(settings.FPS) / 1000  # Delta time in seconds
        current_time = pygame.time.get_ticks() / 1000  # Current game time in seconds

        # Handle events (input, etc.)
        running = handle_events(bird, screen, sound_effects, font, dt)

        # Update background
        background.update(dt)
        background.draw(screen)

        # Update bird
        bird.update_with_dt(dt)

        # Handle game mechanics (e.g., power-ups, events)
        handle_game_mechanics(screen, bird, obstacles, quantum_elements, event_timers, current_time)

        # Quantum Elements Spawning Logic
        if len(quantum_elements) < 1 and random.random() < QUANTUM_PROBABILITY:
            quantum_element = spawn_quantum_element(level_config, settings.WIDTH, settings.HEIGHT)
            if quantum_element:
                quantum_elements.append(quantum_element)
                logging.debug("Quantum element spawned.")

        # Update and draw obstacles
        update_obstacles_with_dt(level_config, obstacles, score, current_level, dt)
        draw_game_elements(screen, bird, obstacles, quantum_elements)

        # Check collisions
        if check_collisions(bird, obstacles, quantum_elements):
            handle_collision(bird, sound_effects.get('collision'))
            update_leaderboard(screen, score, high_scores)
            if bird.lives <= 0:
                game_over_screen(screen, font, score, high_scores)
                running = False

        # Level progression
        current_level, background, level_config = handle_level_progression(
            score, current_level, background, screen, obstacles, level_config)

        # Update QUANTUM_PROBABILITY if a new level was loaded
        QUANTUM_PROBABILITY = level_config.get('quantum_probability', 0.01)

        # Update score based on passed obstacles
        score = update_score(bird, obstacles, score)

        # Display level-specific story text if on level 1 or level 0
        if current_level in [0, 1]:
            display_level_story(screen, font, story_dict, current_level, sound_effects)

        # Draw HUD
        draw_hud(screen, font, score, high_scores, bird, control_display_timer, current_level)

        # Update display
        pygame.display.flip()

        # Check if bird is off-screen
        if bird.rect.y > settings.HEIGHT or bird.rect.y < 0:
            update_leaderboard(screen, score, high_scores)
            game_over_screen(screen, font, score, high_scores)
            running = False

    # Shut down executor and quit
    executor.shutdown(wait=True)
    pygame.quit()

def update_leaderboard(screen, score, high_scores):
    """
    Updates the leaderboard with the current score.

    Args:
        screen (pygame.Surface): The screen surface for displaying the input box if a new high score is achieved.
        score (int): The current score.
        high_scores (dict): The high score data to be updated.
    """
    if score > high_scores.get('top_score', 0):
        high_scores['top_score'] = score
        high_scores['player'] = get_player_name()
        save_high_scores(high_scores)
        logging.info(f"New high score achieved: {score} by {high_scores['player']}")

if __name__ == "__main__":
    main()
