# quantum_effects.py

import numpy as np
import random
import pygame
import ctypes
from modules.settings import *
QUANTUM_FLAP_STRENGTH = -20

# Load CUDAq shared library
cudaq_lib = ctypes.CDLL('./cudaq_module/cudaq_circuits.so')

class QuantumElement:
    def __init__(self, rect, element_type):
        self.rect = rect
        self.type = element_type

    @staticmethod
    def spawn_random(width, height, black_hole_radius, aurora_radius):
        if random.random() < 0.5:
            rect = pygame.Rect(
                random.randint(0, width - black_hole_radius * 2),
                random.randint(height // 2, height - black_hole_radius * 2),
                black_hole_radius * 2,
                black_hole_radius * 2
            )
            return QuantumElement(rect, 'black_hole')
        else:
            rect = pygame.Rect(
                random.randint(0, width - aurora_radius * 2),
                random.randint(height // 2, height - aurora_radius * 2),
                aurora_radius * 2,
                aurora_radius * 2
            )
            return QuantumElement(rect, 'aurora')

def apply_quantum_flap():
    result = ctypes.c_float()
    cudaq_lib.execute_quantum_flap(ctypes.byref(result))
    return result.value

def adjust_obstacle_speed():
    result = ctypes.c_float()
    cudaq_lib.execute_quantum_obstacle_speed(ctypes.byref(result))
    return result.value

def handle_quantum_event(bird, quantum_element, bird_velocity, flap_power):
    is_falling = True
    if quantum_element and bird.rect.colliderect(quantum_element.rect):
        if quantum_element.type == 'black_hole':
            # Quantum Warp: Teleport bird to a random location
            bird.rect.x = random.randint(0, WIDTH - bird.rect.width)
            bird.rect.y = random.randint(0, HEIGHT - bird.rect.height)
            quantum_element = None  # Remove black hole after use
            bird.velocity = flap_power  # Give another chance
            is_falling = False
            logging.info("Quantum Warp activated: Bird teleported.")
        elif quantum_element.type == 'aurora':
            # Quantum Resurrection or Phase Shift: Reset bird's velocity
            bird.velocity = flap_power
            is_falling = False
            quantum_element = None  # Remove aurora after use
            logging.info("Quantum Aurora activated: Bird's velocity reset.")
    return bird_velocity, is_falling
