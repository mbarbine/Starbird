import pygame
import random
import numpy as np
from quantum_flap import apply_quantum_flap
from settings import *
class QuantumPowerUp:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 30, 30)  # Set the size of the power-up
        self.type = type
        self.color = random.choice([pygame.Color('red'), pygame.Color('blue'), pygame.Color('green')])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def apply_effect(self, bird_velocity, obstacles):
        if self.type == 'quantum_flap_boost':
            return apply_quantum_flap() * 2  # Double the flap power
        elif self.type == 'quantum_time_slow':
            return np.clip(bird_velocity * 0.5, -10, 10)  # Slow down time by halving bird velocity
        elif self.type == 'quantum_shield':
            for obstacle in obstacles:
                obstacle.height = 0  # Destroy all obstacles on screen
        return bird_velocity
