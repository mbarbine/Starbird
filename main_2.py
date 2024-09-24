# main_2.py

import pygame
import sys
import concurrent.futures
import logging
import random
import os
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
from modules.quantum_flap import apply_quantum_flap  # Using corrected function

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_holocron_collection(bird, holocron):
    """Checks if the bird has collected a Holocron."""
    if holocron and holocron.collect(bird.rect):
        logging.info("Holocron collected.")
        bird.apply_power_up("shield")  # Example power-up

def start_screen(screen, font):
    """Displays the Start Screen."""
    screen.fill(START_SCREEN_COLOR)  # Dark blue start screen
    title_text = font.render("Starbird", True, BLUE)
    instruction_text = font.render("Press any key to start", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return  # Start the game

def game_over_screen(screen, font, score, high_scores):
    """Displays the Game Over screen."""
    screen.fill(GAME_OVER_COLOR)  # Dark red game over screen
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_scores['top_score']} by {high_scores['player']}", True, WHITE)
    retry_text = font.render("Press R to Retry or Q to Quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def pause_game(screen, font):
    """Pauses the game and waits until the player resumes."""
    paused = True
    pause_text = font.render("Paused. Press P to Resume.", True, WHITE)
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

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

    # Display the Star Wars-style intro
    intro_text = """Welcome to Starbird
Prepare for an epic adventure across the galaxy."""
    star_wars_intro(intro_text, screen)

    # Initialize game variables
    current_level = STARTING_LEVEL
    score = 0
    high_scores = load_high_scores()
    bird = Bird()

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
    holocron = Holocron(WIDTH, HEIGHT) if Holocron else None

    # Initialize thread pool executor for handling quantum events
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    # Get quantum probability from level config
    QUANTUM_PROBABILITY = level_config.get('quantum_probability', 0.01)  # Reduced frequency

    # Load sound effects
    flap_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', FLAP_SOUND))
    collision_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', HIT_SOUND))
    shield_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', SHIELD_SOUND))
    lightsaber_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', LASER_SOUND))
    # Add more sounds as needed

    # Set sound volumes
    flap_sound.set_volume(SFX_VOLUME)
    collision_sound.set_volume(SFX_VOLUME)
    shield_sound.set_volume(SFX_VOLUME)
    lightsaber_sound.set_volume(SFX_VOLUME)

    # Play background music
    if os.path.exists(os.path.join('assets', BACKGROUND_MUSIC)):
        pygame.mixer.music.load(os.path.join('assets', BACKGROUND_MUSIC))
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    else:
        logging.error(f"Background music file {BACKGROUND_MUSIC} not found.")

    running = True

    # Main game loop
    while running:
        clock.tick(FPS)

        # Update background
        background.update()
        background.draw(screen)

        # Event handling
        running = handle_events(bird, screen, flap_sound, shield_sound, lightsaber_sound, font)

        # Update bird
        bird.update()

        # Handle quantum events
        if quantum_elements:
            for quantum_element in quantum_elements:
                executor.submit(quantum_event_task, bird, quantum_element)

        # Quantum Elements Spawning Logic
        if len(quantum_elements) < 1 and random.random() < QUANTUM_PROBABILITY:  # Limit to 1 element max
            quantum_element = spawn_quantum_element(level_config, WIDTH, HEIGHT)
            if quantum_element:
                quantum_elements.append(quantum_element)
                logging.debug("Quantum element spawned.")

        # Update and draw obstacles
        update_obstacles(level_config, obstacles, score, current_level)
        draw_game_elements(screen, bird, obstacles, quantum_elements, holocron)

        # Handle game mechanics
        check_holocron_collection(bird, holocron)
        random_dark_side_event(obstacles, bird, screen)  # Pass the screen argument
        random_jedi_training(screen, bird)
        random_hyperspace_event(bird)

        # Check collisions
        if check_collisions(bird, obstacles, quantum_elements):
            handle_collision(bird)
            update_leaderboard(score, high_scores)
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

        # Update score
        score += 1

        # Draw HUD
        draw_hud(screen, font, score, high_scores)

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

def handle_quantum_event(bird, quantum_element):
    """
    Handles the interaction between the bird and a quantum element.

    Args:
        bird (Bird): The bird object.
        quantum_element (QuantumElement): The quantum element to interact with.
    """
    try:
        # Use apply_quantum_flap to modify velocity with quantum effect
        bird.velocity = apply_quantum_flap()  # Correct function call
        logging.debug("Quantum event handled successfully.")
    except Exception as e:
        logging.error(f"Error in handle_quantum_event: {e}")

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

def handle_events(bird, screen, flap_sound, shield_sound, lightsaber_sound, font):
    """Handles user input and events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            logging.info("Quit event detected.")
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_game(screen, font)
            elif event.key == pygame.K_SPACE and not bird.is_flapping:
                bird.flap()
                flap_sound.play()  # Play flap sound
            elif event.key == pygame.K_s:
                if not bird.shield_active and bird.shield_duration == 0:
                    bird.apply_power_up("shield")
                    shield_sound.play()  # Play shield activation sound
            elif event.key == pygame.K_l:
                if not bird.lightsaber_active:
                    bird.apply_power_up("lightsaber")
                    lightsaber_sound.play()  # Play lightsaber sound
    return True

def activate_special_ability(bird):
    """
    Activates the bird's special ability based on current ability type.
    For example: shield, laser, speed boost.
    """
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
        handle_quantum_event(bird, quantum_element)
    except Exception as e:
        logging.error(f"Error in quantum event task: {e}")

def update_obstacles(level_config, obstacles, score, current_level):
    """Updates obstacle positions and spawns new obstacles as needed."""
    for obstacle in obstacles:
        if hasattr(obstacle, 'update'):
            obstacle.update()
        else:
            logging.error(f"Obstacle {obstacle} does not have an 'update' method.")
    
    spawn_interval = level_config.get('pipe_spawn_rate_fr_frames', PIPE_SPAWN_RATE_FRAMES)
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
    # Play collision sound here if sounds are implemented

CONTROL_DISPLAY_TIME = 5000
control_display_timer = pygame.time.get_ticks()

def draw_hud(screen, font, score, high_scores):
    """Draws the Heads-Up Display (HUD) on the screen."""
    draw_text(f"Score: {score}", font, BLUE, 10, 10, screen)
    draw_text(f"High Score: {high_scores['top_score']} by {high_scores['player']}", font, RED, 10, 50, screen)
    if pygame.time.get_ticks() - control_display_timer < CONTROL_DISPLAY_TIME:
        draw_text("WASD: Move, Space: Flap, S: Shield, L: Lightsaber", font, WHITE, 10, HEIGHT - 50, screen)

def update_leaderboard(score, high_scores):
    """Updates the leaderboard with the current score."""
    if score > high_scores['top_score']:
        high_scores['top_score'] = score
        high_scores['player'] = get_player_name()
        save_high_scores(high_scores)
        logging.info(f"New high score achieved: {score} by {high_scores['player']}")

def get_player_name():
    """Prompts the player to enter their name."""
    # Implement a simple input mechanism or use a text input field
    # For simplicity, returning a placeholder name
    return "Player1"

def save_high_scores(high_scores):
    """Saves the high scores to a file."""
    try:
        with open(os.path.join('assets', HIGH_SCORE_FILE), 'w') as f:
            f.write(f"{high_scores['player']}:{high_scores['top_score']}\n")
        logging.info("High scores saved successfully.")
    except IOError as e:
        logging.error(f"Error saving high scores: {e}")

def load_high_scores():
    """Loads the high scores from a file."""
    high_scores = {'player': 'None', 'top_score': 0}
    try:
        with open(os.path.join('assets', HIGH_SCORE_FILE), 'r') as f:
            line = f.readline().strip()
            if line:
                player, score = line.split(':')
                high_scores['player'] = player
                high_scores['top_score'] = int(score)
                logging.info(f"High score loaded: {high_scores['top_score']} by {high_scores['player']}")
    except FileNotFoundError:
        logging.warning(f"High score file {HIGH_SCORE_FILE} not found. Creating a new one.")
        save_high_scores(high_scores)
    except Exception as e:
        logging.error(f"Error loading high scores: {e}")
    return high_scores

def handle_level_progression(score, current_level, background, screen, obstacles, level_config):
    """Handles level progression based on the score."""
    LEVEL_THRESHOLD_VALUE = LEVEL_THRESHOLD  # Defined in settings.py

    if score != 0 and score % LEVEL_THRESHOLD_VALUE == 0:
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

        # Increase difficulty
        global PIPE_SPEED
        PIPE_SPEED += 0.5  # Increase speed by 0.5 each level
        global PIPE_SPAWN_RATE_FRAMES
        PIPE_SPAWN_RATE_FRAMES = max(30, PIPE_SPAWN_RATE_FRAMES - 10)  # Decrease spawn rate, min 30

        return current_level, background, new_level_config
    else:
        return current_level, background, level_config

def random_dark_side_event(obstacles, bird, screen):
    """Randomly triggers a Dark Side event."""
    if random.randint(0, 99) < 2:
        if dark_side_choice(screen):  # Pass the screen argument
            for obstacle in obstacles:
                obstacle.speed += 1
            logging.info("Dark Side event triggered: Increased obstacle speed.")
        else:
            bird.apply_power_up("shield")
            logging.info("Dark Side event triggered: Shield activated.")

def random_jedi_training(screen, bird):
    """Randomly triggers a Jedi Training event."""
    if random.randint(0, 99) < 5:
        success = jedi_training(screen)  # Corrected to pass only screen
        if success:
            bird.apply_power_up("shield")
            logging.info("Jedi Training succeeded: Shield activated.")
        else:
            bird.velocity += GRAVITY * 1.5
            logging.info("Jedi Training failed: Bird velocity increased.")

def random_hyperspace_event(bird):
    """Randomly triggers a hyperspace event."""
    if random.randint(0, 99) < 5:
        new_x = random.randint(50, WIDTH - 50)
        new_y = random.randint(50, HEIGHT - 50)
        bird.rect.x = new_x
        bird.rect.y = new_y
        bird.velocity = 0
        logging.info(f"Hyperspace jump: Bird teleported to ({new_x}, {new_y}).")

if __name__ == "__main__":
    main()
