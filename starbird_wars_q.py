import pygame
import numpy as np
import subprocess
import ctypes
from modules.quantum_flap import apply_quantum_flap
from modules.hyperspace_jump import activate_hyperspace_jump
from quantum_decision import quantum_decision
from physics import apply_gravity_gpu
from starfighter_selection import select_starfighter
from force_lightning import activate_force_lightning
from force_shield import activate_force_shield
from holocron import Holocron
from dark_side import dark_side_choice
from jedi_training import jedi_training
from death_star import death_star_battle
from level_loader import load_level, get_level_background, get_obstacle_speed, add_obstacle, spawn_quantum_element
from modules.settings import *
from story import read_story_text

# Initialize Pygame
pygame.init()

# Load initial level
current_level = STARTING_LEVEL  # Starting with level 1
level_module = load_level(current_level)

# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starbird Wars Q")

# Load assets
bird_image = pygame.image.load('assets/bird1.png')
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

background_image = pygame.image.load(get_level_background(level_module))

# Starfighter Selection
selected_starfighter = select_starfighter()
bird_image = selected_starfighter.image
bird_ability = selected_starfighter.ability

# Bird (Player)
bird = pygame.Rect(WIDTH // 4, HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
bird_velocity = 0
is_falling = False

# Obstacles
obstacles = []
obstacle_speed = get_obstacle_speed(level_module)

# Quantum Elements
quantum_element = None

# Holocron
holocron = Holocron(WIDTH, HEIGHT)

# Load high score
high_score = load_high_score()

# Font for text rendering
font = pygame.font.Font(None, FONT_SIZE)

# Initialize GPU resources
bird_position = np.array([bird.y], dtype=np.float32)
bird_velocity_array = np.array([bird_velocity], dtype=np.float32)

# Read and display story text
def display_story_text(line_number):
    story_text = read_story_text('story.txt', line_number)
    draw_text(story_text, font, WHITE, WIDTH // 4, HEIGHT // 4)
    pygame.display.flip()
    pygame.time.wait(3000)

def draw_obstacles():
    for top_obstacle, bottom_obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, top_obstacle)
        pygame.draw.rect(screen, BLACK, bottom_obstacle)

def draw_quantum_element(element):
    if element:
        if element.type == 'black_hole':
            color = BLACK
            radius = BLACK_HOLE_RADIUS
        else:
            color = PURPLE
            radius = AURORA_RADIUS
        pygame.draw.circle(screen, color, element.rect.center, radius)


def read_story_text(filename, line_number):
    with open(filename, 'r') as file:
        lines = file.readlines()
        if line_number < len(lines):
            return lines[line_number].strip()
        return "End of Story."



def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def check_holocron_collection():
    if holocron.collect(bird):
        # Apply quantum effects based on the collected Holocron
        if bird_ability == 'Shield':
            activate_force_shield(bird)
        elif bird_ability == 'Laser':
            activate_force_lightning(obstacles)
        elif bird_ability == 'Speed':
            bird_velocity_array[0] += 2

def random_dark_side_event():
    if np.random.randint(0, 100) < 5:  # 5% chance to trigger
        if dark_side_choice():
            # Dark Side powers
            obstacle_speed += 2
            activate_force_push(obstacles)
        else:
            # Light Side bonus
            activate_force_shield(bird)

def random_jedi_training():
    if np.random.randint(0, 100) < 15:  # 15% chance to trigger
        if jedi_training():
            # Reward for success
            activate_force_shield(bird)
        else:
            # Penalty for failure
            bird_velocity_array[0] += GRAVITY * 2

def quantum_flap():
    global bird_velocity_array
    bird_velocity_array[0] = apply_quantum_flap()

def activate_special_ability():
    if bird_ability == 'Shield':
        activate_force_shield(bird)
    elif bird_ability == 'Laser':
        activate_force_lightning(obstacles)
    elif bird_ability == 'Speed':
        bird_velocity_array[0] += 2

def trigger_death_star_battle():
    if current_level == 3:  # Example condition
        death_star_battle(screen, bird)

def random_hyperspace_event():
    if np.random.randint(0, 100) < 5:  # 5% chance to trigger
        activate_hyperspace_jump(screen)

# Main game loop
running = True
story_line = 0  # Initialize the story line number
score = 0  # Initialize the score
while running:
    clock.tick(FPS)
    screen.blit(background_image, (0, 0))
    
    # Apply GPU-accelerated gravity
    apply_gravity_gpu(bird_position, bird_velocity_array, GRAVITY)
    bird.y = int(bird_position[0])
    bird_velocity = bird_velocity_array[0]
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_falling:
                quantum_flap()
            if event.key == pygame.K_a:
                activate_special_ability()

    # Draw obstacles, quantum elements, and other gameplay elements
    draw_obstacles()
    draw_quantum_element(quantum_element)
    holocron.draw(screen)
    
    # Quantum-enhanced events
    check_holocron_collection()
    random_dark_side_event()
    random_jedi_training()
    random_hyperspace_event()

    # Handle collisions and level progression
    for top_obstacle, bottom_obstacle in obstacles:
        if bird.colliderect(top_obstacle) or bird.colliderect(bottom_obstacle):
            is_falling = True
            bird_velocity_array[0] = 0
            quantum_element = spawn_quantum_element(level_module, WIDTH, HEIGHT)
            break

    # Death Star battle at specific levels
    trigger_death_star_battle()



    # Display the story text at the start of each level
    if score % LEVEL_THRESHOLD == 0 and score != 0:
        story_line += 1
        display_story_text(story_line)

    # Draw bird
    screen.blit(bird_image, bird)

    # Draw score and high score
    draw_text(f"Score: {score}", font, BLUE, 10, 10)
    draw_text(f"High Score: {high_score}", font, RED, 10, 50)

    # Function to update the leaderboard
    def update_leaderboard(score):
        # Placeholder implementation
        # Replace with actual leaderboard update logic
        return score > high_score
    
    # Check if the bird hits the ground or goes off-screen
    if bird.y > HEIGHT or bird.y < 0:
        if update_leaderboard(score):
            high_score = score  # Update in-game high score if new record
        running = False

    # Update the display
    pygame.display.flip()

    # Score update and level progression
    score += 1
    current_level, level_module, obstacle_speed, background_image = handle_level_progression(score, current_level)

# End game
pygame.quit()
