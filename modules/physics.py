import numpy as np
import ctypes

# Load the optimized CUDA physics library
cuda_lib = ctypes.CDLL('./optimized_physics.so')

def apply_gravity_gpu(position, velocity, gravity):
    position_ptr = position.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    velocity_ptr = velocity.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    
    # Run the parallelized CUDA physics kernel
    cuda_lib.run_apply_gravity_parallel(position_ptr, velocity_ptr, gravity, len(position))

# Example usage in the game
bird_position = np.array([bird.y], dtype=np.float32)
bird_velocity = np.array([bird_velocity], dtype=np.float32)

apply_gravity_gpu(bird_position, bird_velocity, GRAVITY)

bird.y = int(bird_position[0])
bird_velocity = bird_velocity[0]
