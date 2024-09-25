# modules/game_utils.py

import pygame
import sys
import os
import logging
import random
from threading import Lock
import modules.settings as settings
from modules.jedi_training import jedi_training
from modules.dark_side import dark_side_choice
from modules.holocron import Holocron
from modules.pipe import Pipe

# Lock for thread safety when modifying bird attributes
bird_lock = Lock()

def init_game_window():
    """Initializes the game window."""
    try:
        screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT),
            pygame.FULLSCREEN if settings.FULLSCREEN else 0
        )
        logging.info("Game window initialized successfully.")
    except pygame.error as e:
        logging.error(f"Error initializing game window: {e}")
        screen = pygame.display.set_mode((800, 600))  # Fallback resolution
        logging.info("Fallback game window initialized at 800x600.")
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

def load_sound(sound_path):
    """Loads a sound from the given path."""
    full_path = os.path.join('assets', 'sounds', sound_path)
    try:
        sound = pygame.mixer.Sound(full_path)
        logging.info(f"Loaded sound: {full_path}")
        return sound
    except pygame.error as e:
        logging.error(f"Failed to load sound {full_path}: {e}")
        return None  # Return None to indicate failure

def play_background_music(music_path='background_music.wav'):
    """Plays background music."""
    full_path = os.path.join('assets', 'sounds', music_path)
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

def save_high_scores(high_scores):
    """Saves the high scores to a file."""
    try:
        with open(os.path.join('assets', 'highscore.txt'), 'w') as f:
            f.write(f"{high_scores['player']}:{high_scores['top_score']}\n")
        logging.info("High scores saved successfully.")
    except IOError as e:
        logging.error(f"Error saving high scores: {e}")

def load_high_scores():
    """Loads the high scores from a file."""
    high_scores = {'player': 'None', 'top_score': 0}
    try:
        with open(os.path.join('assets', 'highscore.txt'), 'r') as f:
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
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen = pygame.display.get_surface()
        screen.fill(settings.GAME_OVER)  # Changed to GAME_OVER color for visibility
        txt_surface = font.render(text, True, color)
        input_box.w = max(200, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

    return text if text else "Player1"

def start_screen(screen, font):
    """Displays the Start Screen."""
    screen.fill(settings.START_SCREEN_COLOR)
    title_text = font.render("Starbird", True, settings.BLUE)
    instruction_text = font.render("Press any key to start", True, settings.WHITE)

    screen.blit(title_text, (settings.WIDTH // 2 - title_text.get_width() // 2, settings.HEIGHT // 3))
    screen.blit(instruction_text, (settings.WIDTH // 2 - instruction_text.get_width() // 2, settings.HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Quit event detected on Start Screen.")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return  # Start the game

def game_over_screen(screen, font, score, high_scores):
    """Displays the Game Over screen."""
    screen.fill(settings.GAME_OVER)
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
                logging.info("Quit event detected on Game Over Screen.")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROL_SETTINGS['retry_key']:
                    logging.info("Retry key pressed. Restarting game.")
                    return 'retry'  # Return 'retry' to indicate retry action
                elif event.key == settings.CONTROL_SETTINGS['quit_key']:
                    logging.info("Quit key pressed on Game Over Screen.")
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
                logging.info("Quit event detected while game is paused.")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROL_SETTINGS['pause_key']:
                    logging.info("Resume key pressed. Resuming game.")
                    paused = False

def update_event_timers(event_timers, current_time):
    """
    Updates the event timers based on the current time.

    Args:
        event_timers (dict): Dictionary of event timers.
        current_time (float): The current game time in seconds.
    """
    for event in event_timers:
        event_timers[event] -= current_time
        if event_timers[event] < 0:
            event_timers[event] = 0  # Prevent negative timers

def check_event_timers(event_timers, event_name):
    """
    Checks if the event timer for a specific event has expired.

    Args:
        event_timers (dict): Dictionary of event timers.
        event_name (str): The event to check.

    Returns:
        bool: True if the event timer has expired, False otherwise.
    """
    return event_timers.get(event_name, 0) <= 0

def reset_bird_position(bird, new_x, new_y):
    """
    Resets the bird's position to a new location and stops its velocity.

    Args:
        bird (Bird): The bird object.
        new_x (int): The new x-coordinate for the bird.
        new_y (int): The new y-coordinate for the bird.
    """
    with bird_lock:
        bird.rect.x = new_x
        bird.rect.y = new_y
        bird.velocity = 0
    logging.info(f"Bird position reset to ({new_x}, {new_y}) and velocity set to 0.")

def load_holocrons(num_holocrons):
    """
    Loads a specified number of holocrons into the game.

    Args:
        num_holocrons (int): The number of holocrons to load.

    Returns:
        list: A list of Holocron objects.
    """
    return [Holocron(random.randint(0, settings.WIDTH), random.randint(0, settings.HEIGHT)) for _ in range(num_holocrons)]

def update_pipes(pipes, dt):
    """
    Updates the position of pipes.

    Args:
        pipes (list): List of Pipe objects.
        dt (float): Delta time for frame consistency.
    """
    for pipe in pipes:
        pipe.update(dt)

def update_obstacles_with_dt(level_config, obstacles, score, current_level, dt):
    """
    Updates the positions of all obstacles based on delta time.

    Args:
        level_config (dict): Current level configuration.
        obstacles (list): List of current obstacles.
        score (int): Current game score.
        current_level (int): Current level number.
        dt (float): Delta time to scale movement speed.
    """
    for obstacle in obstacles:
        if hasattr(obstacle, 'update'):
            obstacle.update(dt)  # Pass 'dt' to the 'update' method
        else:
            logging.error(f"Obstacle {obstacle} does not have an 'update' method.")

def add_obstacle(level_config, obstacles, screen_width):
    """Adds an obstacle to the game."""
    pipe_height = level_config.get('pipe_height', settings.PIPE_HEIGHT)
    pipe_gap = level_config.get('pipe_gap', settings.PIPE_GAP)
    pipe_width = level_config.get('pipe_width', settings.PIPE_WIDTH)
    pipe_speed = level_config.get('pipe_speed', settings.PIPE_SPEED)

    new_pipe = Pipe(screen_width, pipe_speed, pipe_gap)
    obstacles.append(new_pipe)
    logging.info(f"New pipe obstacle added at x={screen_width}.")

def update_score(bird, obstacles, score):
    """Updates the score based on obstacles passed."""
    for obstacle in obstacles:
        # Check if the obstacle is of type Pipe and the bird has passed it
        if isinstance(obstacle, Pipe) and not obstacle.passed:
            if bird.rect.x > obstacle.top_rect.right:
                score += 1
                obstacle.passed = True
                logging.info(f"Score updated: {score}")
    return score

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
        if hasattr(obstacle, 'top_rect') and bird.rect.colliderect(obstacle.top_rect):
            logging.info("Collision detected with top obstacle.")
            collision = True
            break
        if hasattr(obstacle, 'bottom_rect') and bird.rect.colliderect(obstacle.bottom_rect):
            logging.info("Collision detected with bottom obstacle.")
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
    draw_text(f"Score: {score}", font, settings.BLUE, 10, 10, screen)
    draw_text(f"High Score: {high_scores['top_score']} by {high_scores['player']}", font, settings.RED, 10, 50, screen)
    draw_text(f"Level: {current_level}", font, settings.GREEN, 10, 90, screen)
    draw_text(f"Lives: {bird.lives}", font, settings.YELLOW, 10, 130, screen)
    active_ability = bird.get_current_ability()
    if active_ability:
        draw_text(f"Ability: {active_ability}", font, settings.CYAN, 10, 170, screen)
    draw_text(f"Velocity: {bird.velocity:.2f}", font, settings.WHITE, 10, 210, screen)
    if pygame.time.get_ticks() - control_display_timer < settings.CONTROL_DISPLAY_TIME:
        draw_text("Space: Flap, S: Shield, L: Laser, P: Pause", font, settings.WHITE, 10, settings.HEIGHT - 50, screen)

def draw_text(text, font, color, x, y, screen):
    """Helper function to draw text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def update_leaderboard(screen, score, high_scores):
    """Updates the leaderboard with the current score."""
    if score > high_scores['top_score']:
        high_scores['top_score'] = score
        high_scores['player'] = get_player_name()
        save_high_scores(high_scores)
        logging.info(f"New high score achieved: {score} by {high_scores['player']}")

def handle_level_progression(score, current_level, background, screen, obstacles, level_config):
    """Handles level progression based on the score."""
    LEVEL_THRESHOLD_VALUE = settings.LEVEL_THRESHOLD

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

        # Optionally, adjust game settings for higher levels
        settings.PIPE_SPEED += 0.5
        settings.PIPE_SPAWN_RATE_FRAMES = max(60, settings.PIPE_SPAWN_RATE_FRAMES - 20)

        return current_level, background, new_level_config
    else:
        return current_level, background, level_config

def random_dark_side_event(obstacles, bird, screen):
    """Randomly triggers a Dark Side event."""
    if random.randint(0, 99) < 2:  # 2% chance
        if dark_side_choice(screen):
            for obstacle in obstacles:
                obstacle.speed += 1
            logging.info("Dark Side event triggered: Increased obstacle speed.")
        else:
            bird.apply_power_up("shield")
            logging.info("Dark Side event triggered: Shield activated.")

def random_jedi_training(screen, bird):
    """Randomly triggers a Jedi Training event."""
    if random.randint(0, 99) < 5:  # 5% chance
        success = jedi_training(screen)
        if success:
            bird.apply_power_up("shield")
            logging.info("Jedi Training succeeded: Shield activated.")
        else:
            with bird_lock:
                bird.velocity += settings.GRAVITY * 1.5
            logging.info("Jedi Training failed: Bird velocity increased.")
