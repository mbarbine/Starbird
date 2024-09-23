import numpy as np
import ctypes
import os
from modules.settings import *
# Get the absolute path to the shared library
library_path = os.path.join(os.path.dirname(__file__), 'hyperspace_shader.so')

# Load the CUDA shared library
cuda_lib = ctypes.CDLL(library_path)

def activate_hyperspace_jump(screen):
    # Convert Pygame screen surface to NumPy array
    screen_array = pygame.surfarray.array3d(screen)
    screen_ptr = screen_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))

    width, height = screen.get_size()

    # Run the CUDA shader effect
    cuda_lib.run_hyperspace_effect(screen_ptr, width, height, pygame.time.get_ticks())
    
    # Update the Pygame display with the modified screen
    pygame.surfarray.blit_array(screen, screen_array)
    pygame.display.flip()
