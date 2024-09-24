# main_2.py

import pygame
import sys
import concurrent.futures
import logging
import random
import os
from threading import Lock

from modules.bird import Bird
from modules.pipe import Pipe
import modules.settings as settings  # Import settings as a module
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

# Initialize a lock for thread safety when modifying bird attributes
bird_lock = Lock()

def check_holocron_collection(bird, holocron, quantum_elements):
    """Checks if the bird has collected a Holocron."""
    if holocron and holocron.collect(bird.rect):
        logging.info("Holocron collected.")
        bird.apply_power_up("shield")  # Example power-up
        quantum_elements.remove(holocron)  # Remove collected Holocron

def start_screen(screen, font):
    """Displays the Start Screen."""
    screen.fill(settings.START_SCREEN_COLOR)  # Dark blue start screen
    title_text = font.render("Starbird", True, settings.BLUE)
    instruction_text = font.render("Press any key to start", True, settings.WHITE)

    screen.blit(title_text, (settings.WIDTH // 2 - title_text.get_width() // 2, settings.HEIGHT // 3))
    screen.blit(instruction_text, (settings.WIDTH // 2 - instruction_text.get_width() // 2, settings.HEIGHT // 2))
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
    screen.fill(settings.GAME_OVER_COLOR)  # Dark red game over screen
    game_over_text = font.render("Game Over", True, settings.RED)
    score_text = font.render(f"Your Score: {score}", True, settings.WHITE)
    high_score_text = font.render(f"High Score: {high_scores['top_score']} by {high_scores['player']}", True, settings.WHITE)
    retry_text = font.render("Press R to Retry or Q to Quit", True, settings.WHITE)

    screen.blit(game_over_text, (settings.WIDTH // 2 - game_over_text.get_width() // 2, settings.HEIGHT // 4))
    screen.blit(score_text, (settings.WIDTH // 2 - score_text.get_width() // 2, settings.HEIGHT // 2 - 50))
    screen.blit(high_score_text, (settings.WIDTH // 2 - high_score_text.get_width() // 2, settings.HEIGHT // 2))
    screen.blit(retry_text, (settings.WIDTH // 2 - retry_text.get_width() // 2, settings.HEIGHT // 2 + 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROL_SETTINGS['retry_key']:
                    main()  # Restart the game
                elif event.key == settings.CONTROL_SETTINGS['quit_key']:
                    pygame.quit()
                    sys.exit()

def pause_game(screen, font):
    """Pauses the game and waits until the player resumes."""
    paused = True
    pause_text = font.render("Paused. Press P to Resume.", True, settings.WHITE)
    screen.blit(pause_text, (settings.WIDTH // 2 - pause_text.get_width() // 2, settings.HEIGHT // 2))
    pygame.display.flip()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROL_SETTINGS['pause_key']:
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
    current_level = settings.STARTING_LEVEL
    score = 0
    high_scores = load_high_scores()
    bird = Bird()
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

    # Initialize Holocron
    holocron = Holocron(settings.WIDTH, settings.HEIGHT) if Holocron else None
    if holocron:
        quantum_elements.append(holocron)

    # Initialize thread pool executor for handling quantum events
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    # Get quantum probability from level config
    QUANTUM_PROBABILITY = level_config.get('quantum_probability', 0.01)  # Reduced frequency

    # Load sound effects
    flap_sound = load_sound(settings.FLAP_SOUND)
    collision_sound = load_sound(settings.HIT_SOUND)
    shield_sound = load_sound(settings.SHIELD_SOUND)
    lightsaber_sound = load_sound(settings.LASER_SOUND)
    # Add more sounds as needed

    # Set sound volumes
    flap_sound.set_volume(settings.SFX_VOLUME)
    collision_sound.set_volume(settings.SFX_VOLUME)
    shield_sound.set_volume(settings.SFX_VOLUME)
    lightsaber_sound.set_volume(settings.SFX_VOLUME)

    # Play background music
    play_background_music(settings.BACKGROUND_MUSIC)

    running = True

    # Initialize event timers
    event_timers = settings.EVENT_TIMERS.copy()

    # Initialize control display timer
    control_display_timer = pygame.time.get_ticks()

    # Main game loop
    while running:
        clock.tick(settings.FPS)  # Control the game speed to match FPS

        # Update background
        background.update()
        background.draw(screen)

        # Event handling
        running = handle_events(bird, screen, flap_sound, shield_sound, lightsaber_sound, font)

        # Update bird
        bird.update()

        # Handle quantum events
        if quantum_elements:
            for quantum_element in quantum_elements.copy():  # Use copy to avoid modification during iteration
                executor.submit(quantum_event_task, bird, quantum_element)

        # Quantum Elements Spawning Logic
        if len(quantum_elements) < 1 and random.random() < QUANTUM_PROBABILITY:  # Limit to 1 element max
            quantum_element = spawn_quantum_element(level_config, settings.WIDTH, settings.HEIGHT)
            if quantum_element:
                quantum_elements.append(quantum_element)
                logging.debug("Quantum element spawned.")

        # Update and draw obstacles
        update_obstacles(level_config, obstacles, score, current_level)
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

        # Update score
        score += 1

        # Draw HUD
        draw_hud(screen, font, score, high_scores, bird, control_display_timer, current_level)

        # Update display
        pygame.display.flip()

        # Check if bird is off-screen
        if bird.rect.y > settings.HEIGHT or bird.rect.y < 0:
            update_leaderboard(score, high_scores)
            game_over_screen(screen, font, score, high_scores)  # Display Game Over Screen
            running = False

    # Shut down executor and quit
    executor.shutdown(wait=True)
    pygame.quit()

def handle_game_mechanics(screen, bird, obstacles, quantum_elements, event_timers):
    """
    Handles game mechanics such as event triggering with cooldowns.
    """
    # Jedi Training Event
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
    if event_timers['holocron'] <= 0 and random.random() < settings.EVENT_FREQUENCY['holocron_spawn_rate']:
        holocron = Holocron(settings.WIDTH, settings.HEIGHT)
        quantum_elements.append(holocron)
        logging.info("Holocron spawned.")
        event_timers['holocron'] = settings.EVENT_COOLDOWNS['holocron']

def load_sound(sound_path):
    """Loads a sound from the given path."""
    full_path = os.path.join('assets', sound_path)
    try:
        sound = pygame.mixer.Sound(full_path)
        logging.info(f"Loaded sound: {full_path}")
        return sound
    except pygame.error as e:
        logging.error(f"Failed to load sound {full_path}: {e}")
        return pygame.mixer.Sound(None)  # Return a silent sound

def play_background_music(music_path):
    """Plays background music."""
    full_path = os.path.join('assets', music_path)
    if os.path.exists(full_path):
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            logging.info(f"Playing background music: {full_path}")
        except pygame.error as e:
            logging.error(f"Failed to play background music {full_path}: {e}")
    else:
        logging.error(f"Background music file {full_path} not found.")

def handle_quantum_event(bird, quantum_element):
    """
    Handles the interaction between the bird and a quantum element.

    Args:
        bird (Bird): The bird object.
        quantum_element (QuantumElement): The quantum element to interact with.
    """
    try:
        # Use apply_quantum_flap to modify velocity with quantum effect
        with bird_lock:
            bird.velocity = apply_quantum_flap()  # Correct function call
        logging.debug("Quantum event handled successfully.")
    except Exception as e:
        logging.error(f"Error in handle_quantum_event: {e}")

def init_game_window():
    """Initializes the game window."""
    try:
        if settings.FULLSCREEN:
            screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        logging.info("Game window initialized successfully.")
    except pygame.error as e:
        logging.error(f"Error initializing game window: {e}")
        screen = pygame.display.set_mode((800, 600))  # Fallback resolution
    pygame.display.set_caption(settings.WINDOW_TITLE)
    return screen

def load_game_font():
    """Loads the game font."""
    try:
        font = pygame.font.Font(None, settings.FONT_SIZE)
        logging.info("Game font loaded successfully.")
        return font
    except pygame.error as e:
        logging.error(f"Error loading font: {e}")
        return pygame.font.SysFont(None, settings.FONT_SIZE)

def handle_events(bird, screen, flap_sound, shield_sound, lightsaber_sound, font):
    """Handles user input and events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            logging.info("Quit event detected.")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == settings.CONTROL_SETTINGS['pause_key']:
                pause_game(screen, font)
            elif event.key == settings.CONTROL_SETTINGS['flap_key'] and not bird.is_flapping:
                bird.flap()
                flap_sound.play()  # Play flap sound
            elif event.key == settings.CONTROL_SETTINGS['shield_key']:
                if not bird.shield_active and bird.shield_duration == 0:
                    bird.apply_power_up("shield")
                    shield_sound.play()  # Play shield activation sound
            elif event.key == settings.CONTROL_SETTINGS['lightsaber_key']:
                if not bird.lightsaber_active:
                    bird.apply_power_up("lightsaber")
                    lightsaber_sound.play()  # Play lightsaber sound
    return True  # Continue running

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

    spawn_interval = level_config.get('pipe_spawn_rate_frames', settings.PIPE_SPAWN_RATE_FRAMES)
    if score % spawn_interval == 0 and score != 0:
        add_obstacle(level_config, obstacles, settings.WIDTH)
        logging.debug("New obstacle spawned.")

def draw_game_elements(screen, bird, obstacles, quantum_elements):
    """Draws all game elements on the screen."""
    bird.draw(screen)
    draw_obstacles(screen, obstacles)
    draw_quantum_elements(screen, quantum_elements)

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

def draw_hud(screen, font, score, high_scores, bird, control_display_timer, current_level):
    """Draws the Heads-Up Display (HUD) on the screen."""
    draw_text(f"Score: {score}", font, settings.BLUE, 10, 10, screen)
    draw_text(f"High Score: {high_scores['top_score']} by {high_scores['player']}", font, settings.RED, 10, 50, screen)
    draw_text(f"Level: {current_level}", font, settings.GREEN, 10, 90, screen)
    draw_text(f"Lives: {bird.lives}", font, settings.YELLOW, 10, 130, screen)
    active_ability = bird.get_current_ability()
    if active_ability:
        draw_text(f"Ability: {active_ability}", font, settings.CYAN, 10, 170, screen)
    if pygame.time.get_ticks() - control_display_timer < settings.CONTROL_DISPLAY_TIME:
        draw_text("Space: Flap, S: Shield, L: Lightsaber, P: Pause", font, settings.WHITE, 10, settings.HEIGHT - 50, screen)

def update_leaderboard(score, high_scores):
    """Updates the leaderboard with the current score."""
    if score > high_scores['top_score']:
        high_scores['top_score'] = score
        high_scores['player'] = get_player_name()
        save_high_scores(high_scores)
        logging.info(f"New high score achieved: {score} by {high_scores['player']}")

def get_player_name():
    """Prompts the player to enter their name."""
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(settings.WIDTH // 2 - 100, settings.HEIGHT // 2, 200, 50)
    color_inactive = settings.WHITE
    color_active = settings.BLUE
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen = pygame.display.get_surface()
        screen.fill(settings.GAME_OVER_COLOR)  # Use a different background if needed
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text if text else "Player1"

def save_high_scores(high_scores):
    """Saves the high scores to a file."""
    try:
        with open(settings.HIGH_SCORE_FILE, 'w') as f:
            f.write(f"{high_scores['player']}:{high_scores['top_score']}\n")
        logging.info("High scores saved successfully.")
    except IOError as e:
        logging.error(f"Error saving high scores: {e}")

def load_high_scores():
    """Loads the high scores from a file."""
    high_scores = {'player': 'None', 'top_score': 0}
    try:
        with open(settings.HIGH_SCORE_FILE, 'r') as f:
            line = f.readline().strip()
            if line:
                player, score = line.split(':')
                high_scores['player'] = player
                high_scores['top_score'] = int(score)
                logging.info(f"High score loaded: {high_scores['top_score']} by {high_scores['player']}")
    except FileNotFoundError:
        logging.warning(f"High score file {settings.HIGH_SCORE_FILE} not found. Creating a new one.")
        save_high_scores(high_scores)
    except Exception as e:
        logging.error(f"Error loading high scores: {e}")
    return high_scores

def handle_level_progression(score, current_level, background, screen, obstacles, level_config):
    """Handles level progression based on the score."""
    LEVEL_THRESHOLD_VALUE = settings.LEVEL_THRESHOLD  # Defined in settings.py

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
        settings.PIPE_SPEED += 0.5  # Increase speed by 0.5 each level
        settings.PIPE_SPAWN_RATE_FRAMES = max(60, settings.PIPE_SPAWN_RATE_FRAMES - 20)  # Decrease spawn rate, min 60 frames (2 seconds at 30 FPS)

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
            with bird_lock:
                bird.velocity += settings.GRAVITY * 1.5
            logging.info("Jedi Training failed: Bird velocity increased.")

def random_hyperspace_event(bird):
    """Randomly triggers a hyperspace event."""
    if random.randint(0, 99) < 5:
        new_x = random.randint(50, settings.WIDTH - 50)
        new_y = random.randint(50, settings.HEIGHT - 50)
        bird.rect.x = new_x
        bird.rect.y = new_y
        with bird_lock:
            bird.velocity = 0
        logging.info(f"Hyperspace jump: Bird teleported to ({new_x}, {new_y}).")

if __name__ == "__main__":
    main()
