import pygame
import sys
import concurrent.futures
import logging
import random
from modules.bird import Bird
from modules.pipe import Pipe
from modules.settings import *
from modules.force_lightning import activate_force_lightning
from modules.holocron import Holocron
from modules.dark_side import dark_side_choice
from modules.jedi_training import jedi_training
from modules.level_loader import (
    load_level,
    get_level_background,
    add_initial_obstacles,
    spawn_quantum_element,
    handle_level_progression
)
from modules.story import star_wars_intro
from modules.text_effects import draw_text
from modules.backgrounds import ScrollingBackground
from modules.quantum_handler import quantum_event_task
from modules.event_handler import handle_events

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function to run the game."""
    pygame.init()
    screen = init_game_window()
    clock = pygame.time.Clock()
    background = ScrollingBackground()
    star_wars_intro("Welcome to Starbird\nPrepare for an epic adventure across the galaxy.", screen)
    
    font = load_game_font()
    current_level = STARTING_LEVEL
    score = 0
    high_score = load_high_score()
    bird = Bird()

    try:
        level_config = load_level(current_level)
    except Exception as e:
        logging.error(f"Failed to load level {current_level}: {e}")
        pygame.quit()
        sys.exit()

    obstacles = add_initial_obstacles(level_config)
    quantum_elements = []
    holocron = Holocron(WIDTH, HEIGHT) if Holocron else None
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    QUANTUM_PROBABILITY = level_config.get('quantum_probability', 0.005)  # Lower probability

    running = True

    while running:
        dt = clock.tick(FPS) / 1000  # Delta time in seconds
        background.update(dt)
        background.draw(screen)

        running = handle_events(bird, screen)
        bird.update()

        # Handle quantum events
        if quantum_elements:
            for quantum_element in quantum_elements:
                executor.submit(quantum_event_task, bird, quantum_element)

        # Quantum Element Spawning Logic
        if random.random() < QUANTUM_PROBABILITY:
            quantum_element = spawn_quantum_element(level_config, WIDTH, HEIGHT)
            if quantum_element:
                quantum_elements.append(quantum_element)
                logging.debug("Quantum element spawned.")

        update_obstacles(level_config, obstacles, score)
        draw_game_elements(screen, bird, obstacles, quantum_elements, holocron)

        check_holocron_collection(bird, holocron)
        random_dark_side_event(obstacles, bird, screen)
        random_jedi_training(screen, bird)
        random_hyperspace_event(bird)

        if check_collisions(bird, obstacles, quantum_elements):
            handle_collision(bird)
            update_leaderboard(score, high_score)
            running = False

        # Level Progression
        current_level, background, level_config = handle_level_progression(
            score, current_level, background, screen, obstacles, level_config
        )
        QUANTUM_PROBABILITY = level_config.get('quantum_probability', 0.005)

        score += 1
        draw_hud(screen, font, score, high_score)
        pygame.display.flip()

        if bird.rect.y > HEIGHT or bird.rect.y < 0:
            update_leaderboard(score, high_score)
            running = False

    executor.shutdown(wait=True)
    pygame.quit()

# Additional helper functions can be added here...

if __name__ == "__main__":
    main()
