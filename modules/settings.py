# modules/settings.py

import os
import pygame  # Ensure pygame is imported for key constants

# Screen Settings
WIDTH = 800
HEIGHT = 600
WINDOW_HEIGHT = HEIGHT  # Alias for HEIGHT to maintain compatibility
FULLSCREEN = False
WINDOW_TITLE = "Starbird: Quantum Edition"
FPS = 30  # Reduced FPS for slower, more manageable gameplay

# Colors
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
PIPE_COLOR = (34, 139, 34)  # Default green color for pipes
SHIELD_COLOR = (0, 255, 255)  # Cyan for shield
BIRD_COLOR = (255, 215, 0)  # Bright yellow for bird visibility
BACKGROUND_COLOR = (10, 10, 50)  # Dark space color
START_SCREEN_COLOR = (0, 0, 128)  # Dark blue start screen
GAME_OVER_COLOR = (128, 0, 0)  # Dark red game over screen
TEXT_COLOR = WHITE
TEXT_HIGHLIGHT_COLOR = (255, 223, 0)  # Gold highlight

# Game Settings
LEVEL_THRESHOLD = 1000  # Threshold for level progression
PIPE_SPAWN_RATE_FRAMES = 120  # Pipe spawn rate in frames (120 frames at 30 FPS = 4 seconds)
PIPE_WIDTH = 90
PIPE_HEIGHT = 600
PIPE_GAP = 180  # Wider gap for better gameplay
PIPE_SPEED = 3  # Reduced speed of pipes for easier navigation
PIPE_VARIANT_COLORS = [
    (34, 139, 34),
    (107, 142, 35),
    (154, 205, 50),
]  # Variety of green shades

# Physics Settings
GRAVITY = 400  # Increased gravity for noticeable downward acceleration
FLAP_STRENGTH = -300  # Increased flap strength for a significant upward boost
AIR_RESISTANCE = 0.95  # Slightly increased air resistance for smoother control
MAX_VELOCITY = 1000  # Increased max velocity to accommodate higher gravity and flap strength
FLAP_COOLDOWN_TIME = 15  # Increased cooldown to prevent excessive flapping
BOOST_MULTIPLIER = 2.0  # Stronger boost effect

# Bird Settings
BIRD_WIDTH = 80
BIRD_HEIGHT = 42
BIRD_START_X = 100
BIRD_START_Y = HEIGHT // 2
BIRD_FRAMES = [
    'assets/bird1.png',
    'assets/bird2.png',
    'assets/bird3.png',
]  # Animation frames for bird
BIRD_MAX_LIVES = 3  # Standard lives for balanced gameplay
BIRD_RESPAWN_TIME = 60  # Frames to respawn after losing a life
BIRD_INVINCIBILITY_FRAMES = 120  # Invincibility after respawn

# Laser Settings
LASER_COLOR = (255, 69, 0)  # Bright orange for laser
LASER_SPEED = 12  # Speed of laser
LASER_COOLDOWN_TIME = 12  # Cooldown time for laser
LASER_POWER_UP_DURATION = 360  # Duration of laser power-up
LASER_BEAM_WIDTH = 7  # Width of laser beam

# Shield Power-Up Settings
SHIELD_DURATION = 240  # Duration of shield effect
SHIELD_RECHARGE_TIME = 400  # Recharge time for shield
SHIELD_FLASH_EFFECT = True  # Flash effect for shield activation
SHIELD_INVINCIBILITY_FRAMES = 60  # Invincibility after shield is hit

# Background Settings
BACKGROUND_IMAGE = 'background.png'  # Space-themed background image
BACKGROUND_SCROLL_SPEED = 2  # Scroll speed for background
BACKGROUND_LOOP = True  # Loop background images
PARALLAX_EFFECT = True  # Enable parallax scrolling
BACKGROUND_LAYERS = ['layer1.png', 'layer2.png']  # Parallax layer images
BACKGROUND_STAR_ANIMATION = True  # Enable twinkling star effect
NEBULA_EFFECT = True  # Enable nebula background effect
NEBULA_COLOR = (75, 0, 130)  # Nebula color setting
DRAW_BLACK_HOLE = True  # Toggle for drawing black holes

# Black Hole Settings
BLACK_HOLE_RADIUS = 40  # Radius for black hole
BLACK_HOLE_COLOR = (0, 0, 0)  # Black hole color
BLACK_HOLE_GRAVITY = 2.0  # Gravity effect of black hole
BLACK_HOLE_SPAWN_PROBABILITY = 0.05  # Probability of black hole spawning

# Audio Settings
FLAP_SOUND = 'sounds/flap.wav'  # Sound for flapping
SCORE_SOUND = 'sounds/score.wav'  # Sound for scoring
HIT_SOUND = 'sounds/hit.wav'  # Sound for collision
LASER_SOUND = 'sounds/laser.wav'  # Sound for laser
SHIELD_SOUND = 'sounds/shield.wav'  # Sound for shield activation
BACKGROUND_MUSIC = 'sounds/background_music.wav'  # Background music
MUSIC_VOLUME = 0.4  # Volume for music
SFX_VOLUME = 0.6  # Volume for sound effects
MUSIC_FADEOUT_TIME = 500  # Fadeout time for music

# Mandelbrot Settings
MANDELBROT_MAX_ITER = 150
MANDELBROT_ZOOM = 200
FRACTAL_COLOR = (255, 69, 0)  # Bright orange

# Starfield and Comet Effects
STAR_COUNT = 150  # Number of stars in background
STAR_COLOR = (255, 255, 255)  # Color of stars
STAR_SPEED = 1  # Speed of stars for parallax effect
COMET_COLOR = (135, 206, 235)  # Light blue color for comets
COMET_SIZE = 15  # Size of comets
COMET_SPEED = [6, 2]  # Speed of comets (X, Y)

# Quantum Integration Settings
QUANTUM_FLAP_STRENGTH = -15  # Placeholder for quantum flap strength
QUANTUM_MAX_VELOCITY = 25  # Max velocity for quantum events
QUANTUM_ENTROPY = 0.02  # Entropy for quantum effects
CUDA_DISABLED = True  # CUDA flag

# AI Integration Settings
AI_FLAP_TUNING = 1.5  # AI flap tuning factor
AI_DIFFICULTY_SCALING = 1.5  # AI difficulty scaling factor
AI_OBSTACLE_GENERATION = True  # AI obstacle generation toggle
AI_ADAPTIVE_MUSIC = True  # Adaptive music based on gameplay

# Font Settings
FONT_SIZE = 36  # General font size

# High Score Settings
HIGH_SCORE_FILE = os.path.join('assets', 'highscore.txt')  # High score file location
HIGHSCORE_ENCRYPTION_KEY = 'supersecretkey'  # Placeholder key for encryption

# Quantum Circuit and AI Settings (Placeholders)
CUDAQ_CIRCUIT_OPTIMIZATION = None
CUDAQ_ERROR_CORRECTION = None
CUDAQ_ENTANGLEMENT = None
CUDAQ_SUPERPOSITION = None
CUDAQ_QUANTUM_WALK_MOVEMENT = None
CUDAQ_NOISE_REDUCTION = None
CUDAQ_QAOA_OPTIMIZATION = None
CUDAQ_MONTE_CARLO = None
CUDAQ_CRYPTOGRAPHY = None

# Game Progression Settings
STARTING_LEVEL = 1  # Initial level

# Quantum Element Settings
AURORA_RADIUS = 50  # Radius of Aurora element
QBLACKHOLE_SIZE = 50  # Size of quantum black hole
QBLACKHOLE_COLOR = (0, 0, 0)  # Color of quantum black hole
AURORABOREALIS_SIZE = 60  # Size of aurora borealis element
AURORABOREALIS_COLOR = CYAN  # Color of aurora borealis element
HOLOCRON_SIZE = 40  # Size of holocron
HOLOCRON_COLOR = (255, 215, 0)  # Color of holocron

# Event Frequency Settings
EVENT_FREQUENCY = {
    'jedi_training': 0.005,       # Probability per frame (0.5%)
    'dark_side': 0.02,            # Probability per frame (2%)
    'hyperspace': 0.005,          # Probability per frame (0.5%)
    'holocron_spawn_rate': 0.001, # Probability per frame (0.1%)
}

# Event Cooldown Settings (in frames)
EVENT_COOLDOWNS = {
    'jedi_training': 600,   # 20 seconds at 30 FPS
    'dark_side': 1200,      # 40 seconds at 30 FPS
    'hyperspace': 900,      # 30 seconds at 30 FPS
    'holocron': 1500,       # 50 seconds at 30 FPS
}

# Initialize Event Timers
EVENT_TIMERS = {
    'jedi_training': 0,
    'dark_side': 0,
    'hyperspace': 0,
    'holocron': 0,
}

# Control Settings
CONTROL_SETTINGS = {
    'flap_key': pygame.K_SPACE,
    'shield_key': pygame.K_s,
    'lightsaber_key': pygame.K_l,
    'pause_key': pygame.K_p,
    'retry_key': pygame.K_r,
    'quit_key': pygame.K_q,
}

# HUD Settings
CONTROL_DISPLAY_TIME = 100  # Time in milliseconds to display control instructions
