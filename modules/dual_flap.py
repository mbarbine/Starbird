import random
from modules.settings import *
def apply_dual_flap(bird_velocity):
    # Randomly decide between a strong or weak flap
    if random.choice([True, False]):
        bird_velocity = -12  # Stronger flap
    else:
        bird_velocity = -8   # Weaker flap
    return bird_velocity
