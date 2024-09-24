# main_2.py

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
from modules.backgrounds import ScrollingBackground

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function to run the game."""
    pygame.init()
    screen = init_game_window()
    clock = pygame.time.Clock()
    background = ScrollingBackground()
    star_wars_intro(screen)
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
        clock.tick(FPS)
        background.update()
        background.draw(screen)
        running = handle_events(bird, screen)
        bird.update()

        if quantum_elements:
            for quantum_element in quantum_elements:
                executor.submit(quantum_event_task, bird, quantum_element)

        if random.random() < QUANTUM_PROBABILITY:
            quantum_element = spawn_quantum_element(level_config, WIDTH, HEIGHT)
            if quantum_element:
                quantum_elements.append(quantum_element)
                logging.debug("Quantum element spawned.")

        update_obstacles(level_config, obstacles, score, current_level)
        draw_game_elements(screen, bird, obstacles, quantum_elements, holocron)
        check_holocron_collection(bird, holocron)
        random_dark_side_event(obstacles, bird, screen)
        random_jedi_training(screen, bird)
        random_hyperspace_event(bird)

        if check_collisions(bird, obstacles, quantum_elements):
            handle_collision(bird)
            update_leaderboard(score, high_score)
            running = False

        current_level, background, level_config = handle_level_progression(
            score,
            current_level,
            background,
            screen,
            obstacles,
            level_config
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

def handle_quantum_event(bird, quantum_element, current_velocity):
    """Handles the interaction between the bird and a quantum element."""
    if hasattr(quantum_element, 'type'):
        if quantum_element.type == 'black_hole':
            new_velocity = current_velocity * 1.5
            logging.info(f"Interacted with {quantum_element.type}: Velocity increased to {new_velocity}.")
        elif quantum_element.type == 'wormhole':
            new_velocity = current_velocity * 0.5
            logging.info(f"Interacted with {quantum_element.type}: Velocity decreased to {new_velocity}.")
        else:
            new_velocity = current_velocity
            logging.warning(f"Unknown quantum element type: {quantum_element.type}. No effect.")
    else:
        new_velocity = current_velocity
        logging.warning(f"Quantum element does not have a type attribute. No effect.")
    return new_velocity

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
        screen = pygame.display.set_mode((800, 600))
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
    spawn_interval = level_config.get('pipe_spawn_rate', PIPE_SPAWN_RATE)
    if score % spawn_interval == 0 and score != 0:
        add_obstacle(level_config, obstacles, WIDTH)
        logging.debug("New obstacle spawned.")

def draw_game_elements(screen, bird, obstacles, quantum_elements, holocron):
    """Draws all game elements on the screen."""
    bird.draw(screen)
    draw_obstacles(screen, obstacles)
    draw_quantum_elements(screen, quantum_elements)
    if holocron:
        holocron.draw(screen)

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
    logging.info("Handled collision: Bird stopped flapping and velocity reset.")

def draw_hud(screen, font, score, high_score):
    """Draws the Heads-Up Display (HUD) on the screen."""
    draw_text(f"Score: {score}", font, BLUE, 10, 10, screen)
    draw_text(f"High Score: {high_score}", font, RED, 10, 50, screen)

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
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write('0')
        logging.warning(f"High score file not found. Created new file at {HIGH_SCORE_FILE}. Setting high score to 0.")
        return 0
    except Exception as e:
        logging.warning(f"Error loading high score: {e}. Setting high score to 0.")
        return 0

def handle_level_progression(score, current_level, background, screen, obstacles, level_config):
    """Handles level progression based on the score."""
    LEVEL_THRESHOLD = 100

    if score != 0 and score % LEVEL_THRESHOLD == 0:
        current_level += 1
        logging.info(f"Progressing to level {current_level}.")
        try:
            new_level_config = load_level(current_level)
        except Exception as e:
            logging.error(f"Failed to load level {current_level}: {e}")
            return current_level, background, level_config
        
        new_obstacles = add_initial_obstacles(new_level_config)
        if new_obstacles:
            obstacles.extend(new_obstacles)
            logging.info(f"Added {len(new_obstacles)} new obstacles for level {current_level}.")
        
        new_background_path = get_level_background(new_level_config)
        if new_background_path:
            background.load_new_background(new_background_path)
            logging.info(f"Background updated for level {current_level}.")

        return current_level, background, new_level_config
    else:
        return current_level, background, level_config

def check_holocron_collection(bird, holocron):
    """Checks if the bird has collected a Holocron."""
    if holocron and holocron.collect(bird.rect):
        logging.info("Holocron collected.")
        bird.apply_power_up("shield")

def random_dark_side_event(obstacles, bird, screen):
    """Randomly triggers a Dark Side event."""
    if random.randint(0, 99) < 1:  # Lower chance to 1%
        if dark_side_choice():
            for obstacle in obstacles:
                obstacle.speed += 1  # Slower speed increase
            logging.info("Dark Side event triggered: Increased obstacle speed.")
        else:
            bird.apply_power_up("shield")
            logging.info("Dark Side event triggered: Shield activated.")

def random_jedi_training(screen, bird):
    """Randomly triggers a Jedi Training event."""
    if random.randint(0, 99) < 2:  # Lower chance to 2%
        success = jedi_training(screen, WIDTH, HEIGHT, GREEN)
        if success:
            bird.apply_power_up("shield")
            logging.info("Jedi Training succeeded: Shield activated.")
        else:
            bird.velocity += GRAVITY * 1.5  # Reduced velocity increase
            logging.info("Jedi Training failed: Bird velocity increased.")

def random_hyperspace_event(bird):
    """Randomly triggers a hyperspace event."""
    if random.randint(0, 99) < 1:
        new_x = random.randint(50, WIDTH - 50)
        new_y = random.randint(50, HEIGHT - 50)
        bird.rect.x = new_x
        bird.rect.y = new_y
        bird.velocity = 0
        logging.info(f"Hyperspace jump: Bird teleported to ({new_x}, {new_y}).")

if __name__ == "__main__":
    main()
