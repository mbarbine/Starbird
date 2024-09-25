# hyperspace_jump.py

import numpy as np
import ctypes
import os
import pygame  # Added import for Pygame
from modules.settings import *

# Get the absolute path to the shared library
library_path = os.path.join(os.path.dirname(__file__), 'hyperspace_shader.so')

# Load the CUDA shared library
try:
    cuda_lib = ctypes.CDLL(library_path)
except OSError as e:
    print(f"Failed to load CUDA library: {e}")
    cuda_lib = None

def activate_hyperspace_jump(screen):
    if cuda_lib is None:
        print("CUDA library not loaded. Cannot activate hyperspace jump.")
        return

    # Convert Pygame screen surface to NumPy array
    screen_array = pygame.surfarray.array3d(screen)
    screen_ptr = screen_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))

    width, height = screen.get_size()

    # Run the CUDA shader effect
    try:
        cuda_lib.run_hyperspace_effect(screen_ptr, width, height, pygame.time.get_ticks())
    except AttributeError:
        print("The CUDA library does not have the 'run_hyperspace_effect' function.")
        return

    # Update the Pygame display with the modified screen
    pygame.surfarray.blit_array(screen, screen_array)
    pygame.display.flip()
