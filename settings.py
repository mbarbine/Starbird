# Game Window Settings
WINDOW_WIDTH = 800  # Increased resolution for a modern display
WINDOW_HEIGHT = 600  # 16:9 aspect ratio for widescreen
FPS = 75  # Increased FPS for smoother gameplay
FULLSCREEN = True # Toggle for fullscreen mode
WINDOW_TITLE = "Starbird: Quantum Edition"  # Custom window title

# Colors
YELLOW = (255, 255, 0) 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)

# Difficulty Settings
DIFFICULTY_INCREASE = 0.1  # Speed increase per 5 points
MAX_DIFFICULTY = 3.0  # Increased difficulty scaling cap for advanced players
DIFFICULTY_CURVE = "exponential"  # Linear, exponential, or custom curve

# Bird Settings
BIRD_WIDTH = 80  # Slightly larger bird for visibility on high-res screens
BIRD_HEIGHT = 42  # Adjusted proportionally to width
BIRD_START_X = 100  # More space from the left edge
BIRD_START_Y = WINDOW_HEIGHT // 2
BIRD_COLOR = (255, 215, 0)  # Bright yellow for visibility
BIRD_FRAMES = ['assets/bird1.png', 'assets/bird2.png', 'assets/bird3.png']  # Animation frames
BIRD_MAX_LIVES = 5  # More lives for longer gameplay
BIRD_RESPAWN_TIME = 60  # Frames to respawn after losing a life
BIRD_INVINCIBILITY_FRAMES = 120  # Temporary invincibility after respawn

# Pipe Settings
PIPE_WIDTH = 90  # Slightly wider pipes for better pacing
PIPE_HEIGHT = 600  # Increased height for larger gaps
PIPE_GAP = 180  # Wider gap to accommodate increased difficulty scaling
PIPE_SPEED = 5  # Slightly faster to match increased screen size and FPS
PIPE_COLOR = (34, 139, 34)  # Forest green color
PIPE_SPAWN_RATE = 1.2  # Faster spawn rate for more intense gameplay
PIPE_ROTATION_ANGLE = 15  # Random rotation angle for pipes for added challenge
PIPE_VARIANT_COLORS = [(34, 139, 34), (107, 142, 35), (154, 205, 50)]  # Different shades of green for variety

# Physics Settings
GRAVITY = 0.6  # Increased gravity for more responsive controls
FLAP_STRENGTH = -12  # Stronger flap to counter increased gravity
AIR_RESISTANCE = 0.96  # Reduced air resistance for faster descent
MAX_VELOCITY = 20  # Increased max velocity to match the new physics
FLAP_COOLDOWN_TIME = 8  # Reduced cooldown for a more responsive feel
BOOST_MULTIPLIER = 2.0  # Stronger boost for temporary power-ups

# Background Settings
BACKGROUND_IMAGE = 'assets/background.png'  # Enhanced space-themed background
BACKGROUND_SCROLL_SPEED = 2  # Faster background scroll for a sense of speed
BACKGROUND_LOOP = True  # Toggle for looping background
PARALLAX_EFFECT = True  # Enable parallax scrolling for a 3D effect
BACKGROUND_LAYERS = ['assets/layer1.png', 'assets/layer2.png']  # Multi-layer parallax background
BACKGROUND_STAR_ANIMATION = True  # Twinkling stars for added immersion

# Color Settings
BACKGROUND_COLOR = (10, 10, 50)  # Darker space-like color for fallback
START_SCREEN_COLOR = (0, 0, 128)  # Dark blue for the start screen
GAME_OVER_COLOR = (128, 0, 0)  # Dark red for the game over screen
TEXT_COLOR = (255, 255, 255)  # White for general text
TEXT_HIGHLIGHT_COLOR = (255, 223, 0)  # Gold color for highlighted text

# Black Hole Settings
BLACK_HOLE_RADIUS = 40  # Larger radius for a more menacing black hole
BLACK_HOLE_COLOR = (0, 0, 0)  # Pure black for the black hole
BLACK_HOLE_GRAVITY = 2.0  # Stronger gravity to match increased radius
BLACK_HOLE_SINGULARITY_COLOR = (75, 0, 130)  # Indigo center for added visual effect
BLACK_HOLE_EVENT_HORIZON_RADIUS = 50  # Larger event horizon for visual effect
BLACK_HOLE_SPAWN_PROBABILITY = 0.05  # Percentage chance for black hole to spawn instead of a pipe

# Audio Settings
FLAP_SOUND = 'assets/flap.wav'  # Sound when the bird flaps
SCORE_SOUND = 'assets/score.wav'  # Sound when the player scores
HIT_SOUND = 'assets/hit.wav'  # Sound when the bird hits a pipe or the ground
LASER_SOUND = 'assets/laser.wav'  # Sound for laser shooting
BACKGROUND_MUSIC = 'assets/background_music.wav'  # Background music file
MUSIC_VOLUME = 0.4  # Background music volume slightly increased
SFX_VOLUME = 0.6  # Increased sound effects volume for better feedback
MUSIC_FADEOUT_TIME = 500  # Fadeout time in milliseconds for smooth transitions

# High Score File
HIGH_SCORE_FILE = 'assets/highscore.txt'  # File for storing the high score
HIGHSCORE_ENCRYPTION_KEY = 'supersecretkey'  # Simple encryption for high score file

# Mandelbrot Settings (for fractal background effects)
MANDELBROT_MAX_ITER = 150  # Increased iterations for more detailed fractal
MANDELBROT_ZOOM = 200  # Higher zoom level for a more complex visual
FRACTAL_COLOR = (255, 69, 0)  # Bright orange for a more vibrant fractal effect

# Starfield and Comet Effects (for background.py)
STAR_COUNT = 150  # More stars for a denser starfield effect
STAR_COLOR = (255, 255, 255)  # White for consistency
STAR_SPEED = 3  # Slightly faster star movement
COMET_COLOR = (135, 206, 235)  # Light blue comet for contrast
COMET_SIZE = 15  # Larger comet size for emphasis
COMET_SPEED = [6, 2]  # Faster comet for dynamic visuals
NEBULA_EFFECT = True  # Toggle for nebula effect in the background
NEBULA_COLOR = (75, 0, 130)  # Purple nebula for a deep space feel

# Quantum Integration Placeholder (for future CUDAQ features)
QUANTUM_FLAP_STRENGTH = -15  # Placeholder for quantum-driven flap strength
QUANTUM_MAX_VELOCITY = 25  # Placeholder for quantum-tuned maximum velocity
QUANTUM_ENTROPY = 0.02  # Entropy level for quantum randomness

# CUDAQ Algorithm Placeholders
CUDAQ_QUANTUM_WALK = None  # Placeholder for implementing quantum random walk algorithms
CUDAQ_QAOA = None  # Placeholder for implementing Quantum Approximate Optimization Algorithm
CUDAQ_VQE = None  # Placeholder for Variational Quantum Eigensolver for optimizing game parameters
CUDAQ_QFT = None  # Placeholder for Quantum Fourier Transform-based features
CUDAQ_QNN = None  # Placeholder for Quantum Neural Networks integration for AI behavior
CUDAQ_GROVER = None  # Placeholder for Grover's algorithm for searching game state space
CUDAQ_SHOR = None  # Placeholder for Shor's algorithm integration (e.g., for puzzles or decryption in gameplay)
CUDAQ_HEURISTIC_ALGO = None  # Placeholder for quantum heuristic algorithms for game difficulty scaling

# AI Integration Placeholder (for future AI-driven behavior)
AI_FLAP_TUNING = 1.5  # Enhanced AI tuning of the bird's flap behavior
AI_DIFFICULTY_SCALING = 1.5  # Advanced AI-driven difficulty scaling
AI_OBSTACLE_GENERATION = True  # AI-driven dynamic obstacle generation
AI_ADAPTIVE_MUSIC = True  # Adaptive music that changes with game intensity

# Laser Settings (for bird shooting lasers)
LASER_COLOR = (255, 69, 0)  # Bright orange for more vibrant lasers
LASER_SPEED = 12  # Faster lasers for a more dynamic feel
LASER_COOLDOWN_TIME = 12  # Reduced cooldown for faster firing rate
LASER_POWER_UP_DURATION = 360  # Longer duration for laser power-ups
LASER_BEAM_WIDTH = 7  # Wider laser beam for a more powerful look

# Shield Power-Up Settings
SHIELD_COLOR = (0, 255, 255)  # Cyan for the shield around the bird
SHIELD_DURATION = 240  # Longer shield duration
SHIELD_RECHARGE_TIME = 400  # Increased recharge time for balance
SHIELD_FLASH_EFFECT = True  # Flashing effect when the shield is active
SHIELD_INVINCIBILITY_FRAMES = 60  # Extra invincibility frames after shield activation

# Quantum Circuit Optimization
CUDAQ_CIRCUIT_OPTIMIZATION = None  # Placeholder for quantum circuit optimization features

# Quantum Error Correction
CUDAQ_ERROR_CORRECTION = None  # Placeholder for implementing quantum error correction algorithms

# Quantum Entanglement Features
CUDAQ_ENTANGLEMENT = None  # Placeholder for quantum entanglement-based game mechanics

# Quantum Superposition Features
CUDAQ_SUPERPOSITION = None  # Placeholder for quantum superposition-based gameplay elements

# Quantum Walk for Movement
CUDAQ_QUANTUM_WALK_MOVEMENT = None  # Placeholder for implementing quantum walk in bird's movement

# Quantum Noise Reduction
CUDAQ_NOISE_REDUCTION = None  # Placeholder for implementing quantum noise reduction in game physics

# Quantum Optimization (QAOA)
CUDAQ_QAOA_OPTIMIZATION = None  # Placeholder for optimizing game difficulty or player movement using QAOA

# Quantum Monte Carlo Simulation
CUDAQ_MONTE_CARLO = None  # Placeholder for implementing quantum Monte Carlo simulations for random events

# Quantum Cryptography
CUDAQ_CRYPTOGRAPHY = None  # Placeholder for adding quantum cryptography-based features in gameplay

# Game Progression Settings
LEVEL_THRESHOLD = 1000  # Example threshold for level progression

# CUDA Disabled Flag (for temporarily disabling CUDA functionality)
CUDA_DISABLED = True  # Set to True to temporarily disable CUDA features until they are fully developed

# Initial Level and Score Settings
STARTING_LEVEL = 1  # Starting with level 1

# Additional Game Settings
GAP_SIZE = 200  # Gap between top and bottom obstacles

# Gravity and Flap Power
FLAP_POWER = -10

# Font Settings
FONT_SIZE = 36

# Quantum Element Sizes
AURORA_RADIUS = 50

# Window and Game Settings
WIDTH, HEIGHT = 800, 600  # Match the WINDOW_WIDTH and WINDOW_HEIGHT settings

# Ensure consistent gravity and flap power
GRAVITY = 0.6  # Match the main game physics settings
FLAP_POWER = -12  # Match the flap strength in the game physics
