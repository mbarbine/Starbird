import pygame
import numpy as np
import sys
import concurrent.futures
from bird import Bird
from pipe import Pipe
from settings import *
from q_blackhole import QBlackHole
from q_aurorabor import AuroraBorealis
from quantum_flap import apply_quantum_flap, handle_quantum_event
from modules.force_lightning import activate_force_lightning
from modules.force_shield import activate_force_shield
from modules.holocron import Holocron
from modules.dark_side import dark_side_choice
from modules.jedi_training import jedi_training
from modules.death_star import death_star_battle
from modules.level_loader import load_level, get_level_background, get_obstacle_speed, add_obstacle, spawn_quantum_element
from modules.story import star_wars_intro, read_story_text
from modules.text_effects import draw_text

# Define game window properties
# Define bird abilities if they are part of the Bird class
bird_ability = 'None'  # Default ability, can be 'Shield', 'Laser', 'Speed', etc.

# Fallback function for applying gravity
def apply_gravity_fallback(bird_velocity, gravity=GRAVITY):
    return bird_velocity + gravity

# Implement or import handle_level_progression
def handle_level_progression(score, current_level):
    if score % LEVEL_THRESHOLD == 0:
        current_level += 1
        level_module = load_level(current_level)
        obstacle_speed = get_obstacle_speed(level_module)
        try:
            background_image = pygame.image.load(get_level_background(level_module)).convert()
        except Exception as e:
            print(f"Error loading level background: {e}")
            background_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            background_image.fill(BACKGROUND_COLOR)
        return current_level, level_module, obstacle_speed, background_image
    return current_level, None, PIPE_SPEED, None

# Load high score function
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            score = f.read().strip()
            return int(score) if score.isdigit() else 0
    except (FileNotFoundError, ValueError):
        return 0

# Initialize Pygame
pygame.init()

# Load initial level
current_level = STARTING_LEVEL  # Starting with level 1
try:
    level_module = load_level(current_level)
except Exception as e:
    print(f"Error loading level {current_level}: {e}")
    level_module = None  # Fallback to None if level loading fails

# Game window setup with error handling
try:
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
except Exception as e:
    print(f"Error initializing game window: {e}")
    screen = pygame.display.set_mode((800, 600))  # Fallback to default resolution

pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()

# Display the Star Wars-style intro
star_wars_intro(screen)

# Load assets safely with error handling
try:
    background_image = pygame.image.load(BACKGROUND_IMAGE).convert()
except Exception as e:
    print(f"Error loading background image: {e}")
    background_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background_image.fill(BACKGROUND_COLOR)

# Bird (Player) setup
bird = Bird()

# Obstacles setup
obstacles = []
try:
    obstacle_speed = get_obstacle_speed(level_module)
except Exception as e:
    print(f"Error getting obstacle speed: {e}")
    obstacle_speed = PIPE_SPEED  # Fallback to a default value

# Quantum Elements setup
quantum_element = None

# Holocron setup
try:
    holocron = Holocron(WIDTH, HEIGHT)
except Exception as e:
    print(f"Error initializing Holocron: {e}")
    holocron = None  # Fallback to None if initialization fails

# Load high score safely
try:
    high_score = load_high_score()
except Exception as e:
    print(f"Error loading high score: {e}")
    high_score = 0

# Font setup with error handling
try:
    font = pygame.font.Font(None, FONT_SIZE)
except Exception as e:
    print(f"Error loading font: {e}")
    font = pygame.font.SysFont(None, FONT_SIZE)

# Thread Pool Executor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)  # Adjust the number of workers as needed

def quantum_event_task(bird, quantum_element):
    try:
        bird.velocity = handle_quantum_event(bird.rect, quantum_element, bird.velocity)
    except Exception as e:
        print(f"Error in quantum event task: {e}")

# Function to read and display story text
def display_story_text(line_number):
    try:
        story_text = read_story_text('story.txt', line_number)
        draw_text(story_text, font, WHITE, WIDTH // 4, HEIGHT // 4, screen)
        pygame.display.flip()
        pygame.time.wait(3000)
    except Exception as e:
        print(f"Error displaying story text: {e}")

# Function to draw obstacles
def draw_obstacles():
    try:
        for obstacle in obstacles:
            if isinstance(obstacle, pygame.Rect):
                pygame.draw.rect(screen, PIPE_COLOR, obstacle)
            else:
                print(f"Invalid obstacle detected: {obstacle}")
    except Exception as e:
        print(f"Error drawing obstacles: {e}")

# Function to draw quantum elements
def draw_quantum_element(element):
    try:
        if element:
            if element.type == 'black_hole':
                color = BLACK
                radius = BLACK_HOLE_RADIUS
            else:
                color = PURPLE
                radius = AURORA_RADIUS
            pygame.draw.circle(screen, color, element.rect.center, radius)
    except Exception as e:
        print(f"Error drawing quantum element: {e}")

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    try:
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
    except Exception as e:
        print(f"Error drawing text: {e}")

# Function to handle Holocron collection
def check_holocron_collection():
    try:
        if holocron and holocron.collect(bird.rect):
            if bird.shield_active:
                activate_force_shield(bird.rect)
            elif bird_ability == 'Laser':
                activate_force_lightning(obstacles)
            elif bird_ability == 'Speed':
                bird.velocity += 2
    except Exception as e:
        print(f"Error handling Holocron collection: {e}")

# Function to trigger random Dark Side events
def random_dark_side_event():
    try:
        if np.random.randint(0, 100) < 5:  # 5% chance to trigger
            if dark_side_choice():
                global obstacle_speed
                obstacle_speed += 2
            else:
                activate_force_shield(bird.rect)
    except Exception as e:
        print(f"Error triggering Dark Side event: {e}")

# Function to trigger random Jedi Training events
def random_jedi_training():
    try:
        if np.random.randint(0, 100) < 15:  # 15% chance to trigger
            if jedi_training(screen, WIDTH, HEIGHT, GREEN):
                activate_force_shield(bird.rect)
            else:
                bird.velocity += GRAVITY * 2
    except Exception as e:
        print(f"Error triggering Jedi Training event: {e}")

# Function to trigger the Death Star battle
def trigger_death_star_battle():
    try:
        if current_level == 3:  # Example condition
            death_star_battle(screen, bird.rect)
    except Exception as e:
        print(f"Error triggering Death Star battle: {e}")

# Function to trigger random hyperspace events
def random_hyperspace_event():
    try:
        if np.random.randint(0, 100) < 5:  # 5% chance to trigger
            pass  # Implement hyperspace jump functionality here
    except Exception as e:
        print(f"Error triggering hyperspace event: {e}")

# Main game loop
running = True
story_line = 0  # Initialize the story line number
score = 0

while running:
    clock.tick(FPS)
    screen.blit(background_image, (0, 0))

    # Update bird position and state
    bird.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not bird.is_flapping:
                bird.flap()
            elif event.key == pygame.K_a:
                activate_special_ability()

    # Submit quantum event handling task to the thread pool
    try:
        executor.submit(quantum_event_task, bird, quantum_element)
    except Exception as e:
        print(f"Error submitting quantum event task: {e}")

    # Draw obstacles, quantum elements, and other gameplay elements
    try:
        draw_obstacles()
        draw_quantum_element(quantum_element)
        if holocron:
            holocron.draw(screen)
    except Exception as e:
        print(f"Error drawing game elements: {e}")

    # Quantum-enhanced events
    try:
        check_holocron_collection()
        random_dark_side_event()
        random_jedi_training()
        random_hyperspace_event()
    except Exception as e:
        print(f"Error handling quantum-enhanced events: {e}")

    # Handle collisions and level progression
    try:
        if any(bird.rect.colliderect(obstacle) for obstacle in obstacles) or (quantum_element and bird.rect.colliderect(quantum_element.rect)):
            bird.is_flapping = False
            bird.velocity = 0
            quantum_element = spawn_quantum_element(level_module, WIDTH, HEIGHT)
    except Exception as e:
        print(f"Error handling collision or level progression: {e}")

    # Death Star battle at specific levels
    try:
        trigger_death_star_battle()
    except Exception as e:
        print(f"Error triggering Death Star battle: {e}")

    # Display the story text at the start of each level
    if score % LEVEL_THRESHOLD == 0 and score != 0:
        try:
            story_line += 1
            display_story_text(story_line)
        except Exception as e:
            print(f"Error displaying story text: {e}")

    # Draw bird
    try:
        bird.draw(screen)
    except Exception as e:
        print(f"Error drawing bird: {e}")

    # Draw score and high score
    try:
        draw_text(f"Score: {score}", font, BLUE, 10, 10)
        draw_text(f"High Score: {high_score}", font, RED, 10, 50)
    except Exception as e:
        print(f"Error drawing score text: {e}")

    # Check if the bird hits the ground or goes off-screen
    if bird.rect.y > HEIGHT or bird.rect.y < 0:
        try:
            def update_leaderboard(score):
                # Implement leaderboard update functionality here
                return False  # Example return value

            if update_leaderboard(score):
                high_score = score  # Update in-game high score if new record
        except Exception as e:
            print(f"Error updating leaderboard: {e}")
        running = False

    # Update the display
    pygame.display.flip()

    # Score update and level progression
    try:
        score += 1
        current_level, level_module, obstacle_speed, new_background_image = handle_level_progression(score, current_level)
        if new_background_image:
            background_image = new_background_image
    except Exception as e:
        print(f"Error updating score or progressing level: {e}")

# Shut down the executor
try:
    executor.shutdown(wait=True)
except Exception as e:
    print(f"Error shutting down executor: {e}")

# End game
pygame.quit()
