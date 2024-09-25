# modules/settings.py

import os
import pygame

# -------------------------------
# Screen Settings
# -------------------------------
WIDTH = 800
HEIGHT = 600
FULLSCREEN = False
WINDOW_TITLE = "Starbird: Quantum Edition"
FPS = 60

# -------------------------------
# Color Settings
# -------------------------------
COLORS = {
    'YELLOW': (255, 255, 0),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'BLUE': (0, 0, 255),
    'GREEN': (0, 255, 0),
    'ORANGE': (255, 165, 0),
    'CYAN': (0, 255, 255),
    'PURPLE': (128, 0, 128),
    'PIPE': (34, 139, 34),
    'SHIELD': (0, 255, 255),
    'BIRD': (255, 215, 0),
    'BACKGROUND': (10, 10, 50),
    'START_SCREEN': (0, 0, 128),
    'GAME_OVER': (128, 0, 0),
    'TEXT': (255, 255, 255),
    'TEXT_HIGHLIGHT': (255, 223, 0),
}

# -------------------------------
# Game Settings
# -------------------------------
LEVEL_THRESHOLD = 1000
PIPE_SPAWN_RATE_FRAMES = 120
PIPE_WIDTH = 90
PIPE_HEIGHT = 600
PIPE_GAP = 180
PIPE_SPEED = 3  # Global pipe speed for consistency
PIPE_VARIANT_COLORS = [
    (34, 139, 34),
    (107, 142, 35),
    (154, 205, 50),
]
PIPE_COLOR = PIPE_VARIANT_COLORS[0]

# -------------------------------
# Scrolling Settings
# -------------------------------
SCROLL_SPEED = 2  # Speed at which the text scrolls during the intro

# -------------------------------
# Physics Settings
# -------------------------------
GRAVITY = 0.15
FLAP_STRENGTH = -6
AIR_RESISTANCE = 0.99
MAX_VELOCITY = 8
MIN_VELOCITY = -8
ROTATION_SCALING = 4
BIRD_ROTATION_LIMIT = 60
FLAP_COOLDOWN_TIME = 12

# -------------------------------
# Bird Settings
# -------------------------------
BIRD_COLOR = COLORS['BIRD']
BIRD_WIDTH = 80
BIRD_HEIGHT = 42
BIRD_START_X = 100
BIRD_START_Y = HEIGHT // 2
BIRD_FRAMES = [
    os.path.join('assets', 'bird1.png'),
    os.path.join('assets', 'bird2.png'),
    os.path.join('assets', 'bird3.png'),
]
BIRD_MAX_LIVES = 3
BIRD_RESPAWN_TIME = 60
BIRD_INVINCIBILITY_FRAMES = 120

# -------------------------------
# Background Settings
# -------------------------------
BACKGROUND_IMAGE = os.path.join('assets', 'background.png')
BACKGROUND_SCROLL_SPEED = 2
BACKGROUND_LAYERS = [
    os.path.join('assets', 'layer1.png'),
    os.path.join('assets', 'layer2.png')
]
STAR_COUNT = 150
STAR_COLOR = COLORS['WHITE']
STAR_SPEED = 1
DRAW_BLACK_HOLE = True
BLACK_HOLE_COLOR = COLORS['BLACK']
BLACK_HOLE_RADIUS = 40

# -------------------------------
# Comet Settings
# -------------------------------
COMET_COLOR = (135, 206, 235)
COMET_SIZE = 15
COMET_SPEED = [6, 2]

# -------------------------------
# Sound and Music Settings
# -------------------------------
SOUNDS = {
    'FLAP': os.path.join('assets', 'sounds', 'flap.wav'),
    'SCORE': os.path.join('assets', 'sounds', 'score.wav'),
    'HIT': os.path.join('assets', 'sounds', 'hit.wav'),
    'LASER': os.path.join('assets', 'sounds', 'laser.wav'),
    'SHIELD': os.path.join('assets', 'sounds', 'shield.wav'),
    'BACKGROUND_MUSIC': os.path.join('assets', 'sounds', 'background_music.wav'),
    'LIGHTSABER': os.path.join('assets', 'sounds', 'lightsaber.wav'),
}
MUSIC_VOLUME = 0.75
SFX_VOLUME = 0.8
MUSIC_FADEOUT_TIME = 500

# -------------------------------
# Laser Settings
# -------------------------------
LASER_COOLDOWN_TIME = 60  # Time in frames for laser cooldown
LASER_COLOR = COLORS['BIRD']  # Color of the laser, matching the bird color
LIGHTSABER_COLOR = COLORS['GREEN']  # Defined color for the lightsaber
LIGHTSABER_LENGTH = 100  # Example value for the length of the lightsaber

# -------------------------------
# Control Settings
# -------------------------------
CONTROL_SETTINGS = {
    'flap_key': pygame.K_SPACE,
    'shield_key': pygame.K_s,
    'lightsaber_key': pygame.K_l,
    'pause_key': pygame.K_p,
    'retry_key': pygame.K_r,
    'quit_key': pygame.K_q,
}

# -------------------------------
# Event Settings
# -------------------------------
EVENT_FREQUENCY = {
    'jedi_training': 0.0005,
    'dark_side': 0.002,
    'hyperspace': 0.0005,
    'holocron_spawn_rate': 0.0001,
}
EVENT_COOLDOWNS = {
    'jedi_training': 1200,
    'dark_side': 1900,
    'hyperspace': 1800,
    'holocron': 3000,
}
EVENT_TIMERS = {key: 0 for key in EVENT_FREQUENCY}

# -------------------------------
# Holocron Settings
# -------------------------------
HOLOCRON_SETTINGS = {
    'size': 40,
    'color': COLORS['CYAN'],
    'speed': PIPE_SPEED,
}

# -------------------------------
# HUD and Display Settings
# -------------------------------
HUD_SETTINGS = {
    'font_size': 36,
    'text_color': COLORS['TEXT'],
    'text_highlight_color': COLORS['TEXT_HIGHLIGHT'],
    'control_display_time': 100,  # Time in milliseconds for control instructions display
    'scroll_speed': 2,
}
CONTROL_DISPLAY_TIME = 5000  # Time in milliseconds to show control instructions

# -------------------------------
# Game and AI Settings
# -------------------------------
STARTING_LEVEL = 1
AI_SETTINGS = {
    'flap_tuning': 1.5,
    'difficulty_scaling': 1.5,
    'obstacle_generation': True,
    'adaptive_music': True,
}

# -------------------------------
# Quantum Integration Settings
# -------------------------------
QUANTUM_SETTINGS = {
    'flap_strength': -20,
    'max_velocity': 15,
    'entropy': 0.002,
    'black_hole_radius': 40,
    'black_hole_color': COLORS['BLACK'],
    'aurora_radius': 50,
    'aurora_color': COLORS['CYAN'],
}
QUANTUM_FLAP_STRENGTH = QUANTUM_SETTINGS['flap_strength']
QUANTUM_FLAP_SCALING_FACTOR = 1.5
QUANTUM_FLAP_VARIANTS = {
    'standard': QUANTUM_FLAP_STRENGTH,
    'boost': QUANTUM_FLAP_STRENGTH * 1.2,
    'reduced': QUANTUM_FLAP_STRENGTH * 0.8,
}
QUANTUM_FLAP_PROBABILITY = 0.1

# -------------------------------
# Miscellaneous Settings
# -------------------------------
FONT_SIZE = 36
HIGH_SCORE_FILE = os.path.join('assets', 'highscore.txt')
HIGHSCORE_ENCRYPTION_KEY = 'supersecretkey'

# -------------------------------
# Start Screen Color
# -------------------------------
START_SCREEN_COLOR = COLORS['START_SCREEN']
BACKGROUND_MUSIC = os.path.join('assets', 'sounds', 'background_music.wav')

# -------------------------------
# Animation Settings
# -------------------------------
ANIMATION_SPEED = 0.1  # Speed for bird animation
AURORA_RADIUS = 50
# -------------------------------
# Power-Up Settings
# -------------------------------
SHIELD_DURATION = 5000  # Shield duration in millisecond
SHIELD_COLOR = COLORS['SHIELD']
SHIELD_PULSE_SPEED = 0.1
SHIELD_PULSE_AMPLITUDE = 10
SHIELD_PULSE_OFFSET = 0
SHIELD_PULSE_DIRECTION = 1
SHIELD_PULSE_MIN = 0
CONTROL_SETTINGS = {
    'flap_key': pygame.K_SPACE,
    'shield_key': pygame.K_s,
    'lightsaber_key': pygame.K_l,
    'pause_key': pygame.K_p,
    'retry_key': pygame.K_r,
    'quit_key': pygame.K_q,
}