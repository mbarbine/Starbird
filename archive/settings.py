# modules/settings.py

import os
import pygame

# -------------------------------
# Screen Settings
# -------------------------------
WIDTH = 1024  # Adjusted width for balanced resolution
HEIGHT = 768  # Adjusted height for balanced resolution
FULLSCREEN = False  # Disabled fullscreen for easier testing
WINDOW_TITLE = "Starbird: Quantum Edition"
FPS = 60  # Maintained for smooth gameplay

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
    'BACKGROUND': (10, 10, 50),  # Slightly lighter for better visibility
    'START_SCREEN': (0, 0, 128),
    'GAME_OVER': (128, 0, 0),
    'TEXT': (255, 255, 255),
    'TEXT_HIGHLIGHT': (255, 223, 0),
    'LASER': (0, 255, 0),  # Green laser color
}

# -------------------------------
# Game Settings
# -------------------------------
LEVEL_THRESHOLD = 800  # Lowered threshold for quicker level progression
PIPE_SPAWN_RATE_FRAMES = 60  # Increased spawn rate for more obstacles
PIPE_WIDTH = 80  # Reduced width for easier navigation
PIPE_HEIGHT = 600
PIPE_GAP = 150  # Reduced gap for balanced difficulty
PIPE_SPEED = 4  # Reduced speed to slow down the game

PIPE_VARIANT_COLORS = [
    (34, 139, 34),
    (107, 142, 35),
    (154, 205, 50),
]
PIPE_COLOR = PIPE_VARIANT_COLORS[0]

# -------------------------------
# Scrolling Settings
# -------------------------------
SCROLL_SPEED = 2  # Reduced scroll speed to slow down the game

# -------------------------------
# Physics Settings
# -------------------------------
GRAVITY = 1.0  # Increased gravity for noticeable downward movement
FLAP_STRENGTH = -12  # Stronger flap to counteract increased gravity
AIR_RESISTANCE = 0.98  # Reduced air resistance for smoother movement
MAX_VELOCITY = 15  # Increased max velocity for dynamic motion
MIN_VELOCITY = -15  # Increased min velocity for stronger flaps
ROTATION_SCALING = 5  # Enhanced rotation effect
BIRD_ROTATION_LIMIT = 45  # Reduced rotation limit for better visuals
FLAP_COOLDOWN_TIME = 10  # Maintained cooldown for balanced flap frequency

# -------------------------------
# Bird Settings
# -------------------------------
BIRD_COLOR = COLORS['BIRD']
BIRD_WIDTH = 50  # Further reduced width for better maneuverability
BIRD_HEIGHT = 30  # Further reduced height for better maneuverability
BIRD_START_X = 150  # Positioned slightly to the right for better visibility
BIRD_START_Y = HEIGHT // 2
BIRD_FRAMES = [
    os.path.join('assets', 'bird1.png'),
    os.path.join('assets', 'bird2.png'),
    os.path.join('assets', 'bird3.png'),
]
BIRD_MAX_LIVES = 5  # Increased lives for better playability
BIRD_RESPAWN_TIME = 90  # Increased respawn time for balance
BIRD_INVINCIBILITY_FRAMES = 150  # Increased invincibility duration

# -------------------------------
# Background Settings
# -------------------------------
BACKGROUND_IMAGE = os.path.join('assets', 'background.png')
BACKGROUND_SCROLL_SPEED = 2  # Reduced scroll speed to slow down the game
BACKGROUND_LAYERS = [
    os.path.join('assets', 'layer1.png'),
    os.path.join('assets', 'layer2.png'),
]
STAR_COUNT = 250  # Further increased number of stars for richness
STAR_COLOR = COLORS['WHITE']
STAR_SPEED = 1  # Reduced star speed to slow down the game
DRAW_BLACK_HOLE = True
BLACK_HOLE_COLOR = COLORS['BLACK']
BLACK_HOLE_RADIUS = 50  # Increased radius for visual impact

# -------------------------------
# Comet Settings
# -------------------------------
COMET_COLOR = (135, 206, 235)
COMET_SIZE = 25  # Further increased size for better visibility
COMET_SPEED = [5, 2]  # Reduced speed to slow down the game

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
MUSIC_VOLUME = 0.80  # Slightly reduced for balance
SFX_VOLUME = 0.85  # Balanced sound effects
MUSIC_FADEOUT_TIME = 700  # Increased fadeout time for smoother transitions

# -------------------------------
# Laser Settings
# -------------------------------
LASER_COOLDOWN_TIME = 25  # Further reduced cooldown for rapid firing
LASER_COLOR = COLORS['LASER']  # Ensured consistent laser color
LASER_SPEED = 15  # Added speed setting for lasers
LASER_DAMAGE = 25  # Added damage setting for balance
LASER_WIDTH = 5  # Added width for visual representation
LIGHTSABER_COLOR = COLORS['GREEN']  # Consistent lightsaber color
LIGHTSABER_LENGTH = 120  # Increased length for better visuals
LIGHTSABER_DURATION = 10000  # Increased duration for power-up effectiveness

# -------------------------------
# Power-Up Settings
# -------------------------------
SHRINK_SCALE = 0.7  # Reduced scale factor for noticeable effect
SHIELD_DURATION = 7000  # Further increased shield duration for better protection
SHIELD_COLOR = COLORS['SHIELD']
SHIELD_PULSE_SPEED = 0.15  # Increased pulse speed for visual effect
SHIELD_PULSE_AMPLITUDE = 15  # Increased amplitude for stronger pulses
SHIELD_PULSE_OFFSET = 0

SLOWDOWN_DURATION = 7000  # Further increased slowdown duration for better gameplay
SLOWDOWN_AIR_RESISTANCE = 0.90  # Reduced air resistance factor during slowdown for noticeable effect

# -------------------------------
# Control Settings
# -------------------------------
CONTROL_SETTINGS = {
    'flap_key': pygame.K_SPACE,
    'shield_key': pygame.K_s,
    'laser_key': pygame.K_l,       # Reintroduced laser key
    'lightsaber_key': pygame.K_f,  # Ensured accessibility
    'pause_key': pygame.K_p,
    'retry_key': pygame.K_r,
    'quit_key': pygame.K_q,
}

# -------------------------------
# Event Settings
# -------------------------------
EVENT_FREQUENCY = {
    'jedi_training': 0.0005,  # Reduced frequency for fewer events
    'dark_side': 0.004,        # Increased frequency for dynamic gameplay
    'hyperspace': 0.002,       # Further increased frequency for variety
    'holocron_spawn_rate': 0.0003,  # Further increased spawn rate for collectibles
}
EVENT_COOLDOWNS = {
    'jedi_training': 1500,  # Increased cooldown for fewer occurrences
    'dark_side': 1400,       # Further reduced cooldown for dynamic challenges
    'hyperspace': 1300,      # Further reduced cooldown for variety
    'holocron': 2000,        # Further reduced cooldown for collectible balance
}
EVENT_TIMERS = {key: 0 for key in EVENT_FREQUENCY}

# -------------------------------
# Holocron Settings
# -------------------------------
HOLOCRON_SETTINGS = {
    'size': 35,  # Reduced size for better integration
    'color': COLORS['CYAN'],
    'speed': PIPE_SPEED + 1,  # Slightly faster for challenge
}

# -------------------------------
# HUD and Display Settings
# -------------------------------
HUD_SETTINGS = {
    'font_size': 32,  # Slightly reduced for better fit
    'text_color': COLORS['TEXT'],
    'text_highlight_color': COLORS['TEXT_HIGHLIGHT'],
    'control_display_time': 150,  # Increased display time for readability
    'scroll_speed': SCROLL_SPEED,
}
CONTROL_DISPLAY_TIME = 6000  # Increased time in milliseconds to show control instructions

# -------------------------------
# Game and AI Settings
# -------------------------------
STARTING_LEVEL = 1
AI_SETTINGS = {
    'flap_tuning': 1.6,  # Slightly increased tuning for better AI performance
    'difficulty_scaling': 1.8,  # Further increased difficulty scaling
    'obstacle_generation': True,
    'adaptive_music': True,
}

# -------------------------------
# Quantum Integration Settings
# -------------------------------
QUANTUM_SETTINGS = {
    'flap_strength': -30,  # Further increased flap strength for quantum flaps
    'max_velocity': 18,     # Further increased max velocity for dynamic motion
    'entropy': 0.003,       # Slightly increased entropy for unpredictability
    'black_hole_radius': 50,  # Consistent with background settings
    'black_hole_color': COLORS['BLACK'],
    'aurora_radius': 60,    # Increased radius for visual effect
    'aurora_color': COLORS['CYAN'],
}
QUANTUM_FLAP_STRENGTH = QUANTUM_SETTINGS['flap_strength']
QUANTUM_FLAP_SCALING_FACTOR = 1.6  # Slightly increased scaling factor
QUANTUM_FLAP_VARIANTS = {
    'standard': QUANTUM_FLAP_STRENGTH,
    'boost': QUANTUM_FLAP_STRENGTH * 1.3,  # Increased boost factor
    'reduced': QUANTUM_FLAP_STRENGTH * 0.7,  # Adjusted reduced factor
}
QUANTUM_FLAP_PROBABILITY = 0.15  # Increased probability for more frequent quantum flaps
QUANTUM_FLAP_COOLDOWN_TIME = 1.5  # Reduced cooldown time for quicker usage

# -------------------------------
# Miscellaneous Settings
# -------------------------------
FONT_SIZE = 32  # Ensured consistency with HUD settings
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
ANIMATION_SPEED = 0.15  # Increased speed for smoother animations
AURORA_RADIUS = QUANTUM_SETTINGS['aurora_radius']
STORY_FILE_PATH = os.path.join('assets', 'story', 'story.md')
STORY_MD_PATH = os.path.join('assets', 'story', 'story.md') 