# settings.py

import os  # Import the os module

# Game Window Settings
WINDOW_WIDTH = 800  # Increased resolution for a modern display
WINDOW_HEIGHT = 600  # 4:3 aspect ratio for consistency
FPS = 75  # Increased FPS for smoother gameplay
FULLSCREEN = False  # Toggle for fullscreen mode
WINDOW_TITLE = "Starbird: Quantum Edition"  # Custom window title

# Colors
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Difficulty Settings
DIFFICULTY_INCREASE = 0.1  # Speed increase per 5 points
MAX_DIFFICULTY = 3.0  # Increased difficulty scaling cap
DIFFICULTY_CURVE = "exponential"  # Linear, exponential, or custom curve

# Bird Settings
BIRD_WIDTH = 80  # Larger bird for high-res screens
BIRD_HEIGHT = 42  # Adjusted proportionally to width
BIRD_START_X = 100  # More space from the left edge
BIRD_START_Y = WINDOW_HEIGHT // 2
BIRD_COLOR = (255, 215, 0)  # Bright yellow for visibility
BIRD_FRAMES = [
    'assets/bird1.png',
    'assets/bird2.png',
    'assets/bird3.png',
]  # Animation frames
BIRD_MAX_LIVES = 3  # Standard lives for gameplay balance
BIRD_RESPAWN_TIME = 60  # Frames to respawn after losing a life
BIRD_INVINCIBILITY_FRAMES = 120  # Invincibility after respawn

# Pipe Settings
PIPE_WIDTH = 90  # Wider pipes for better pacing
PIPE_HEIGHT = 600  # Increased height
PIPE_GAP = 180  # Wider gap for increased difficulty
PIPE_SPEED = 5  # Matches increased screen size and FPS
PIPE_COLOR = (34, 139, 34)  # Forest green
PIPE_SPAWN_RATE = 1.2  # Faster spawn rate
PIPE_ROTATION_ANGLE = 15  # Random rotation angle
PIPE_VARIANT_COLORS = [
    (34, 139, 34),
    (107, 142, 35),
    (154, 205, 50),
]  # Variety of green shades

# Physics Settings
GRAVITY = 0.6  # Increased gravity
FLAP_STRENGTH = -12  # Stronger flap
AIR_RESISTANCE = 0.96  # Reduced air resistance
MAX_VELOCITY = 20  # Increased max velocity
FLAP_COOLDOWN_TIME = 8  # Reduced cooldown
BOOST_MULTIPLIER = 2.0  # Stronger boost

# Background Settings
BACKGROUND_IMAGE = 'assets/background.png'  # Space-themed background
BACKGROUND_SCROLL_SPEED = 2  # Faster scroll speed
BACKGROUND_LOOP = True  # Looping background
PARALLAX_EFFECT = True  # Enable parallax scrolling
BACKGROUND_LAYERS = ['assets/layer1.png', 'assets/layer2.png']  # Parallax layers
BACKGROUND_STAR_ANIMATION = True  # Twinkling stars

# Additional Background Effects
NEBULA_EFFECT = True  # Enable nebula effect
NEBULA_COLOR = (75, 0, 130)  # Purple nebula
DRAW_BLACK_HOLE = True  # Toggle black hole drawing

# Color Settings
BACKGROUND_COLOR = (10, 10, 50)  # Dark space color
START_SCREEN_COLOR = (0, 0, 128)  # Dark blue start screen
GAME_OVER_COLOR = (128, 0, 0)  # Dark red game over screen
TEXT_COLOR = (255, 255, 255)  # White text
TEXT_HIGHLIGHT_COLOR = (255, 223, 0)  # Gold highlight

# Black Hole Settings
BLACK_HOLE_RADIUS = 40  # Larger radius
BLACK_HOLE_COLOR = (0, 0, 0)  # Pure black
BLACK_HOLE_GRAVITY = 2.0  # Stronger gravity
BLACK_HOLE_SINGULARITY_COLOR = (75, 0, 130)  # Indigo center
BLACK_HOLE_EVENT_HORIZON_RADIUS = 50  # Larger event horizon
BLACK_HOLE_SPAWN_PROBABILITY = 0.05  # Spawn chance

# Audio Settings
FLAP_SOUND = 'assets/flap.wav'
SCORE_SOUND = 'assets/score.wav'
HIT_SOUND = 'assets/hit.wav'
LASER_SOUND = 'assets/laser.wav'
BACKGROUND_MUSIC = 'assets/background_music.wav'
MUSIC_VOLUME = 0.4  # Adjusted volume
SFX_VOLUME = 0.6  # Adjusted SFX volume
MUSIC_FADEOUT_TIME = 500  # Fadeout time

# High Score File
HIGH_SCORE_FILE = 'assets/highscore.txt'
HIGHSCORE_ENCRYPTION_KEY = 'supersecretkey'  # Placeholder key

# Mandelbrot Settings
MANDELBROT_MAX_ITER = 150
MANDELBROT_ZOOM = 200
FRACTAL_COLOR = (255, 69, 0)  # Bright orange

# Starfield and Comet Effects
STAR_COUNT = 150  # More stars
STAR_COLOR = (255, 255, 255)
STAR_SPEED = 1  # Adjusted for parallax effect
COMET_COLOR = (135, 206, 235)  # Light blue comet
COMET_SIZE = 15  # Larger comet
COMET_SPEED = [6, 2]  # Faster comet

# Quantum Integration Placeholder
QUANTUM_FLAP_STRENGTH = -15  # Placeholder value
QUANTUM_MAX_VELOCITY = 25
QUANTUM_ENTROPY = 0.02

# Quantum Placeholders
CUDAQ_QUANTUM_WALK = None
CUDAQ_QAOA = None
CUDAQ_VQE = None
CUDAQ_QFT = None
CUDAQ_QNN = None
CUDAQ_GROVER = None
CUDAQ_SHOR = None
CUDAQ_HEURISTIC_ALGO = None

# AI Integration Placeholder
AI_FLAP_TUNING = 1.5
AI_DIFFICULTY_SCALING = 1.5
AI_OBSTACLE_GENERATION = True
AI_ADAPTIVE_MUSIC = True

# Laser Settings
LASER_COLOR = (255, 69, 0)
LASER_SPEED = 12
LASER_COOLDOWN_TIME = 12
LASER_POWER_UP_DURATION = 360
LASER_BEAM_WIDTH = 7

# Shield Power-Up Settings
SHIELD_COLOR = (0, 255, 255)
SHIELD_DURATION = 240
SHIELD_RECHARGE_TIME = 400
SHIELD_FLASH_EFFECT = True
SHIELD_INVINCIBILITY_FRAMES = 60

# Quantum Circuit Optimization
CUDAQ_CIRCUIT_OPTIMIZATION = None

# Quantum Error Correction
CUDAQ_ERROR_CORRECTION = None

# Quantum Entanglement Features
CUDAQ_ENTANGLEMENT = None

# Quantum Superposition Features
CUDAQ_SUPERPOSITION = None

# Quantum Walk for Movement
CUDAQ_QUANTUM_WALK_MOVEMENT = None

# Quantum Noise Reduction
CUDAQ_NOISE_REDUCTION = None

# Quantum Optimization (QAOA)
CUDAQ_QAOA_OPTIMIZATION = None

# Quantum Monte Carlo Simulation
CUDAQ_MONTE_CARLO = None

# Quantum Cryptography
CUDAQ_CRYPTOGRAPHY = None

# Game Progression Settings
LEVEL_THRESHOLD = 1000

# CUDA Disabled Flag
CUDA_DISABLED = True

# Initial Level and Score Settings
STARTING_LEVEL = 1

# Additional Game Settings
GAP_SIZE = 200

# Gravity and Flap Power
GRAVITY = 0.6  # Match physics settings
FLAP_POWER = -12

# Font Settings
FONT_SIZE = 36

# Quantum Element Sizes
AURORA_RADIUS = 50

# Window and Game Settings
WIDTH, HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT

# Gravity and Flap Power
GRAVITY = 0.6
FLAP_POWER = -12
# settings.py

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
PIPE_COLOR = (34, 139, 34)  # Green
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font settings
FONT_SIZE = 36

# High score file
HIGH_SCORE_FILE = 'high_score.txt'

# Pipe settings
PIPE_WIDTH = 80
GAP_SIZE = 200
PIPE_SPEED = 5

# Quantum Elements settings
QBLACKHOLE_SIZE = 50
QBLACKHOLE_COLOR = (0, 0, 0)  # Black
AURORABOREALIS_SIZE = 60
AURORABOREALIS_COLOR = (0, 255, 255)  # Cyan
HOLOCRON_SIZE = 40
HOLOCRON_COLOR = (255, 215, 0)  # Gold
# settings.py

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
PIPE_COLOR = (34, 139, 34)  # Green
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SHIELD_COLOR = (0, 255, 255)  # Cyan for shield
BIRD_COLOR = (255, 255, 255)  # White
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font settings
FONT_SIZE = 36

# High score file
HIGH_SCORE_FILE = os.path.join('assets', 'highscore.txt')  # Updated path

# Pipe settings
PIPE_WIDTH = 80
GAP_SIZE = 200
PIPE_SPEED = 5

# Quantum Elements settings
QBLACKHOLE_SIZE = 50
QBLACKHOLE_COLOR = (0, 0, 0)  # Black
AURORABOREALIS_SIZE = 60
AURORABOREALIS_COLOR = (0, 255, 255)  # Cyan

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

# Physics settings
GRAVITY = 0.5
AIR_RESISTANCE = 0.98
MAX_VELOCITY = 10
FLAP_STRENGTH = 10
FLAP_COOLDOWN_TIME = 15  # Frames
SHIELD_DURATION = 180  # Frames (3 seconds at 60 FPS)
LASER_COOLDOWN_TIME = 120  # Frames (2 seconds at 60 FPS)

# Holocron settings
HOLOCRON_SIZE = 30
