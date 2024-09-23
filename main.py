# main_2.py

import pygame
import sys
import concurrent.futures
import logging
import random  # Added for random events
from modules.bird import Bird
from modules.pipe import Pipe
from modules.settings import *
from modules.force_lightning import activate_force_lightning
# from modules.force_shield import activate_force_shield  # Not needed if handled within Bird
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
from modules.story import star_wars_intro, read_story_text
from modules.text_effects import draw_text
from modules.backgrounds import ScrollingBackground  # Adjusted import based on directory structure

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_holocron_collection(bird, holocron):
    """Checks if the bird has collected a Holocron."""
    if holocron and holocron.collect(bird.rect):
        logging.info("Holocron collected.")
        # Implement holocron effects, e.g., granting abilities or power-ups
        bird.apply_power_up("shield")  # Example power-up


def main():
    """Main function to run the game."""
    # Initialize Pygame
    pygame.init()

    # Game window setup
    screen = init_game_window()
    clock = pygame.time.Clock()

    # Initialize Scrolling Background
    background = ScrollingBackground()

    # Display the Star Wars-style intro
    star_wars_intro(screen)

    # Load game font
    font = load_game_font()

    # Initialize game variables
    current_level = STARTING_LEVEL
    score = 0
    high_score = load_high_score()
    bird = Bird()

    # Load level configuration
    try:
        level_config = load_level(current_level)
    except Exception as e:
        logging.error(f"Failed to load level {current_level}: {e}")
        pygame.quit()
        sys.exit()

    # Initialize obstacles
    obstacles = add_initial_obstacles(level_config, current_level)

    # Initialize quantum elements
    quantum_elements = []  # Separate list for quantum elements

    # Initialize Holocron
    holocron = Holocron(WIDTH, HEIGHT) if Holocron else None

    # Initialize thread pool executor for handling quantum events
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    # Get quantum probability from level config
    QUANTUM_PROBABILITY = level_config.get('quantum_probability', 0.1)  # Default to 0.1 if not set

    running = True
    story_line = 0

    # Main game loop
    while running:
        clock.tick(FPS)

        # Update background
        background.update()
        background.draw(screen)

        # Event handling
        running = handle_events(bird, screen)

        # Update bird
        bird.update()

        # Handle quantum events
        if quantum_elements:
            for quantum_element in quantum_elements:
                executor.submit(quantum_event_task, bird, quantum_element)

        # Quantum Elements Spawning Logic
        if random.random() < QUANTUM_PROBABILITY:
            quantum_element = spawn_quantum_element(level_config, WIDTH, HEIGHT)
            if quantum_element:
                quantum_elements.append(quantum_element)
                logging.debug("Quantum element spawned.")

        # Update and draw obstacles
        update_obstacles(level_config, obstacles, score, current_level)
        draw_game_elements(screen, bird, obstacles, quantum_elements, holocron)

        # Handle game mechanics
        check_holocron_collection(bird, holocron)
        random_dark_side_event(obstacles, bird, screen)  # Pass bird and screen if needed
        random_jedi_training(screen, bird)
        random_hyperspace_event(bird)

        # Check collisions
        if check_collisions(bird, obstacles, quantum_elements):
            handle_collision(bird)
            update_leaderboard(score, high_score)
            running = False

        # Level progression
        current_level, background, level_config = handle_level_progression(
            score,
            current_level,
            background,
            screen,
            obstacles,
            level_config  # Pass the current level_config
        )

        # Update QUANTUM_PROBABILITY if a new level was loaded
        if level_config:
            QUANTUM_PROBABILITY = level_config.get('quantum_probability', 0.1)  # Update with new level's probability

        # Update score
        score += 1

        # Draw HUD
        draw_hud(screen, font, score, high_score)

        # Update display
        pygame.display.flip()

        # Check if bird is off-screen
        if bird.rect.y > HEIGHT or bird.rect.y < 0:
            update_leaderboard(score, high_score)
            running = False

    # Shut down executor and quit
    executor.shutdown(wait=True)
    pygame.quit()


def init_game_window():
    """Initializes the game window."""
    try:
        if FULLSCREEN:
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
        logging.info("Game window initialized successfully.")
    except pygame.error as e:
        logging.error(f"Error initializing game window: {e}")
        screen = pygame.display.set_mode((800, 600))  # Fallback resolution
    pygame.display.set_caption(WINDOW_TITLE)
    return screen


def load_game_font():
    """Loads the game font."""
    try:
        font = pygame.font.Font(None, FONT_SIZE)
        logging.info("Game font loaded successfully.")
        return font
    except pygame.error as e:
        logging.error(f"Error loading font: {e}")
        return pygame.font.SysFont(None, FONT_SIZE)


def handle_events(bird, screen):
    """Handles user input and events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            logging.info("Quit event detected.")
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not bird.is_flapping:
                bird.flap()
            elif event.key == pygame.K_s:
                if not bird.shield_active and bird.shield_duration == 0:
                    bird.apply_power_up("shield")
            elif event.key == pygame.K_l:
                if not bird.lightsaber_active:
                    bird.apply_power_up("lightsaber")
    return True


def activate_special_ability(bird):
    """
    Activates the bird's special ability based on current ability type.
    For example: shield, laser, speed boost.
    """
    ability = bird.get_current_ability()  # Ensure this method exists in Bird class
    logging.info(f"Activating special ability: {ability}")
    if ability == 'Shield':
        bird.apply_power_up("shield")
    elif ability == 'Laser':
        activate_force_lightning(bird.rect)
    elif ability == 'Speed':
        bird.speed_boost()  # Ensure this method exists in Bird class
    else:
        logging.warning(f"Unknown ability: {ability}")


def quantum_event_task(bird, quantum_element):
    """Handles quantum events in a separate thread."""
    try:
        updated_velocity = handle_quantum_event(bird, quantum_element, bird.velocity)
        bird.velocity = updated_velocity
        logging.debug("Quantum event handled successfully.")
    except Exception as e:
        logging.error(f"Error in quantum event task: {e}")


def update_obstacles(level_config, obstacles, score, current_level):
    """Updates obstacle positions and spawns new obstacles as needed."""
    for obstacle in obstacles:
        if hasattr(obstacle, 'update'):
            obstacle.update()
        else:
            logging.error(f"Obstacle {obstacle} does not have an 'update' method.")
    
    # Spawn new obstacles based on spawn rate
    if score % PIPE_SPAWN_RATE == 0 and score != 0:
        add_obstacle(level_config, obstacles, WIDTH)
        logging.debug("New obstacle spawned.")


def draw_game_elements(screen, bird, obstacles, quantum_elements, holocron):
    """Draws all game elements on the screen."""
    bird.draw(screen)
    draw_obstacles(screen, obstacles)
    draw_quantum_elements(screen, quantum_elements)
    if holocron:
        holocron.draw(screen)
    # Draw additional elements like UI overlays if needed


def draw_obstacles(screen, obstacles):
    """Draws all obstacles on the screen."""
    for obstacle in obstacles:
        obstacle.draw(screen)


def draw_quantum_elements(screen, quantum_elements):
    """Draws all quantum elements on the screen."""
    for element in quantum_elements:
        if hasattr(element, 'draw'):
            element.draw(screen)


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


def handle_collision(bird):
    """Handles the collision event."""
    bird.is_flapping = False
    bird.velocity = 0
    # Implement additional collision handling like reducing lives, playing sounds, etc.
    logging.info("Handled collision: Bird stopped flapping and velocity reset.")


def draw_hud(screen, font, score, high_score):
    """Draws the Heads-Up Display (HUD) on the screen."""
    draw_text(f"Score: {score}", font, BLUE, 10, 10, screen)
    draw_text(f"High Score: {high_score}", font, RED, 10, 50, screen)
    # Add more HUD elements like lives, power-up indicators, etc.


def update_leaderboard(score, high_score):
    """Updates the leaderboard with the current score."""
    if score > high_score:
        logging.info(f"New high score achieved: {score}")
        save_high_score(score)


def save_high_score(score):
    """Saves the new high score to a file."""
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(score))
        logging.info("High score saved successfully.")
    except IOError as e:
        logging.error(f"Error saving high score: {e}")


def load_high_score():
    """Loads the high score from a file."""
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            score = f.read().strip()
            high_score = int(score) if score.isdigit() else 0
            logging.info(f"High score loaded: {high_score}")
            return high_score
    except FileNotFoundError:
        # Create the file if it doesn't exist
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write('0')
        logging.warning(f"High score file not found. Created new file at {HIGH_SCORE_FILE}. Setting high score to 0.")
        return 0
    except Exception as e:
        logging.warning(f"Error loading high score: {e}. Setting high score to 0.")
        return 0


def handle_level_progression(score, current_level, background, screen, obstacles, level_config):
    """
    Handles level progression based on the score.

    Args:
        score (int): Current game score.
        current_level (int): Current level number.
        background (ScrollingBackground): Current background object.
        screen (pygame.Surface): Pygame screen surface.
        obstacles (list): List of current obstacles.
        level_config (dict): Current level configuration.

    Returns:
        tuple: (updated_level_number, updated_background, updated_level_config)
    """
    LEVEL_THRESHOLD = 100  # Ensure this constant is defined or imported

    if score != 0 and score % LEVEL_THRESHOLD == 0:
        current_level += 1
        logging.info(f"Progressing to level {current_level}.")
        try:
            new_level_config = load_level(current_level)
        except Exception as e:
            logging.error(f"Failed to load level {current_level}: {e}")
            # Retain the existing level_config if loading fails
            return current_level, background, level_config
        
        new_obstacles = add_initial_obstacles(new_level_config, current_level)
        if new_obstacles:
            obstacles.extend(new_obstacles)
            logging.info(f"Added {len(new_obstacles)} new obstacles for level {current_level}.")
        
        # Update background based on new level
        new_background_path = get_level_background(new_level_config)
        if new_background_path:
            background.load_new_background(new_background_path)
            logging.info(f"Background updated for level {current_level}.")
    
        # Return the new level configuration
        return current_level, background, new_level_config
    else:
        # No level progression; retain the current level_config
        return current_level, background, level_config


def check_holocron_collection(bird, holocron):
    """Checks if the bird has collected a Holocron."""
    if holocron and holocron.collect(bird.rect):
        logging.info("Holocron collected.")
        # Implement holocron effects, e.g., granting abilities or power-ups
        bird.apply_power_up("shield")  # Example power-up


def random_dark_side_event(obstacles, bird, screen):
    """Randomly triggers a Dark Side event."""
    if random.randint(0, 99) < 5:  # 5% chance
        if dark_side_choice():
            for obstacle in obstacles:
                obstacle.speed += 2
            logging.info("Dark Side event triggered: Increased obstacle speed.")
        else:
            bird.apply_power_up("shield")  # Apply shield to bird
            logging.info("Dark Side event triggered: Shield activated.")


def random_jedi_training(screen, bird):
    """Randomly triggers a Jedi Training event."""
    if random.randint(0, 99) < 15:  # 15% chance
        success = jedi_training(screen, WIDTH, HEIGHT, GREEN)
        if success:
            bird.apply_power_up("shield")
            logging.info("Jedi Training succeeded: Shield activated.")
        else:
            bird.velocity += GRAVITY * 2
            logging.info("Jedi Training failed: Bird velocity increased.")


def random_hyperspace_event(bird):
    """Randomly triggers a hyperspace event."""
    if random.randint(0, 99) < 5:  # 5% chance
        # Implement hyperspace jump functionality
        # Example: Teleport bird to a random position
        new_x = random.randint(50, WIDTH - 50)
        new_y = random.randint(50, HEIGHT - 50)
        bird.rect.x = new_x
        bird.rect.y = new_y
        bird.velocity = 0
        logging.info(f"Hyperspace jump: Bird teleported to ({new_x}, {new_y}).")


if __name__ == "__main__":
    main()
