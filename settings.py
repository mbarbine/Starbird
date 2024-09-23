# settings.py

import os  # Import the os module
# settings.py

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Game settings
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10

# Pipe settings
PIPE_WIDTH = 80
GAP_SIZE = 200
PIPE_SPEED = 5

# Window title
WINDOW_TITLE = "Starbird"

# High score file
HIGH_SCORE_FILE = os.path.join('assets', 'high_score.txt')

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen settings
WIDTH = 800
HEIGHT = 600
FULLSCREEN = False
WINDOW_TITLE = "Starbird"

# Game settings
FPS = 60
LEVEL_THRESHOLD = 100  # Example threshold for level progression
PIPE_SPAWN_RATE = 60  # Example spawn rate (spawn a pipe every 60 frames)

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PIPE_COLOR = (34, 139, 34)  # Green
SHIELD_COLOR = (0, 255, 255)  # Cyan for shield
BIRD_COLOR = (255, 255, 255)  # White

# Font settings
FONT_SIZE = 36

# High score file
HIGH_SCORE_FILE = os.path.join('assets', 'highscore.txt')  # Updated path
HIGHSCORE_ENCRYPTION_KEY = 'supersecretkey'  # Placeholder key

# Pipe settings
PIPE_WIDTH = 80
GAP_SIZE = 200
PIPE_SPEED = 5

# Bird settings
BIRD_FRAMES = [
    'assets/bird1.png',
    'assets/bird2.png',
    'assets/bird3.png'
]
BIRD_START_X = WIDTH // 4
BIRD_START_Y = HEIGHT // 2
BIRD_WIDTH = 50
BIRD_HEIGHT = 35
BIRD_MAX_LIVES = 3  # Standard lives for gameplay balance
BIRD_RESPAWN_TIME = 60  # Frames to respawn after losing a life
BIRD_INVINCIBILITY_FRAMES = 120  # Invincibility after respawn

# Physics settings
GRAVITY = 0.6
AIR_RESISTANCE = 0.96
MAX_VELOCITY = 20
FLAP_STRENGTH = -12
FLAP_COOLDOWN_TIME = 8  # Reduced cooldown
BOOST_MULTIPLIER = 2.0  # Stronger boost

# Background settings
BACKGROUND_IMAGE = 'assets/background.png'  # Space-themed background
BACKGROUND_SCROLL_SPEED = 2  # Faster scroll speed
BACKGROUND_LOOP = True  # Looping background
PARALLAX_EFFECT = True  # Enable parallax scrolling
BACKGROUND_LAYERS = ['assets/layer1.png', 'assets/layer2.png']  # Parallax layers
BACKGROUND_STAR_ANIMATION = True  # Twinkling stars

# Additional background effects
NEBULA_EFFECT = True  # Enable nebula effect
NEBULA_COLOR = (75, 0, 130)  # Purple nebula
DRAW_BLACK_HOLE = True  # Toggle black hole drawing

# Color settings
BACKGROUND_COLOR = (10, 10, 50)  # Dark space color
START_SCREEN_COLOR = (0, 0, 128)  # Dark blue start screen
GAME_OVER_COLOR = (128, 0, 0)  # Dark red game over screen
TEXT_COLOR = (255, 255, 255)  # White text
TEXT_HIGHLIGHT_COLOR = (255, 223, 0)  # Gold highlight

# Black hole settings
BLACK_HOLE_RADIUS = 40  # Larger radius
BLACK_HOLE_COLOR = (0, 0, 0)  # Pure black
BLACK_HOLE_GRAVITY = 2.0  # Stronger gravity
BLACK_HOLE_SINGULARITY_COLOR = (75, 0, 130)  # Indigo center
BLACK_HOLE_EVENT_HORIZON_RADIUS = 50  # Larger event horizon
BLACK_HOLE_SPAWN_PROBABILITY = 0.05  # Spawn chance

# Audio settings
FLAP_SOUND = 'assets/flap.wav'
SCORE_SOUND = 'assets/score.wav'
HIT_SOUND = 'assets/hit.wav'
LASER_SOUND = 'assets/laser.wav'
BACKGROUND_MUSIC = 'assets/background_music.wav'
MUSIC_VOLUME = 0.4  # Adjusted volume
SFX_VOLUME = 0.6  # Adjusted SFX volume
MUSIC_FADEOUT_TIME = 500  # Fadeout time

# Mandelbrot settings
MANDELBROT_MAX_ITER = 150
MANDELBROT_ZOOM = 200
FRACTAL_COLOR = (255, 69, 0)  # Bright orange

# Starfield and comet effects
STAR_COUNT = 150  # More stars
STAR_COLOR = (255, 255, 255)
STAR_SPEED = 1  # Adjusted for parallax effect
COMET_COLOR = (135, 206, 235)  # Light blue comet
COMET_SIZE = 15  # Larger comet
COMET_SPEED = [6, 2]  # Faster comet

# Quantum integration placeholder
QUANTUM_FLAP_STRENGTH = -15  # Placeholder value
QUANTUM_MAX_VELOCITY = 25
QUANTUM_ENTROPY = 0.02

# Quantum placeholders
CUDAQ_QUANTUM_WALK = None
CUDAQ_QAOA = None
CUDAQ_VQE = None
CUDAQ_QFT = None
CUDAQ_QNN = None
CUDAQ_GROVER = None
CUDAQ_SHOR = None
CUDAQ_HEURISTIC_ALGO = None

# AI integration placeholder
AI_FLAP_TUNING = 1.5
AI_DIFFICULTY_SCALING = 1.5
AI_OBSTACLE_GENERATION = True
AI_ADAPTIVE_MUSIC = True

# Laser settings
LASER_COLOR = (255, 69, 0)
LASER_SPEED = 12
LASER_COOLDOWN_TIME = 12
LASER_POWER_UP_DURATION = 360
LASER_BEAM_WIDTH = 7

# Shield power-up settings
SHIELD_DURATION = 240
SHIELD_RECHARGE_TIME = 400
SHIELD_FLASH_EFFECT = True
SHIELD_INVINCIBILITY_FRAMES = 60

# Quantum circuit optimization
CUDAQ_CIRCUIT_OPTIMIZATION = None

# Quantum error correction
CUDAQ_ERROR_CORRECTION = None

# Quantum entanglement features
CUDAQ_ENTANGLEMENT = None

# Quantum superposition features
CUDAQ_SUPERPOSITION = None

# Quantum walk for movement
CUDAQ_QUANTUM_WALK_MOVEMENT = None

# Quantum noise reduction
CUDAQ_NOISE_REDUCTION = None

# Quantum optimization (QAOA)
CUDAQ_QAOA_OPTIMIZATION = None

# Quantum Monte Carlo simulation
CUDAQ_MONTE_CARLO = None

# Quantum cryptography
CUDAQ_CRYPTOGRAPHY = None

# Game progression settings
LEVEL_THRESHOLD = 1000

# CUDA disabled flag
CUDA_DISABLED = True

# Initial level and score settings
STARTING_LEVEL = 1

# Additional game settings
GAP_SIZE = 200

# Font settings
FONT_SIZE = 36

# Quantum element sizes
AURORA_RADIUS = 50

# Quantum elements settings
QBLACKHOLE_SIZE = 50
QBLACKHOLE_COLOR = (0, 0, 0)  # Black
AURORABOREALIS_SIZE = 60
AURORABOREALIS_COLOR = (0, 255, 255)  # Cyan
HOLOCRON_SIZE = 30
HOLOCRON_COLOR = (255, 215, 0)  # Gold
