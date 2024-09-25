# modules/quantum_powerups.py

import pygame
import random
import numpy as np
from modules.quantum_flap import apply_quantum_flap
from modules.settings import *

class QuantumPowerUp:
    """
    Represents a quantum power-up that provides special abilities to the bird when collected.
    """

    def __init__(self, x, y, powerup_type):
        """
        Initializes the quantum power-up with a position and type.

        Args:
            x (int): The x-coordinate of the power-up.
            y (int): The y-coordinate of the power-up.
            powerup_type (str): The type of power-up effect.
        """
        self.rect = pygame.Rect(x, y, 30, 30)  # Size of the power-up
        self.type = powerup_type
        self.color = random.choice([pygame.Color('red'), pygame.Color('blue'), pygame.Color('green')])

    def draw(self, screen):
        """
        Draws the power-up on the screen.

        Args:
            screen (pygame.Surface): The Pygame surface to draw on.
        """
        pygame.draw.rect(screen, self.color, self.rect)

    def apply_effect(self, bird, obstacles):
        """
        Applies the effect of the power-up to the bird and obstacles.

        Args:
            bird (Bird): The bird object affected by the power-up.
            obstacles (list): List of current obstacles.

        Returns:
            float: Updated bird velocity after applying the effect.
        """
        if self.type == 'quantum_flap_boost':
            # Boost bird velocity with a quantum flap
            bird.velocity = apply_quantum_flap(bird.velocity, event_type='boost')
            return bird.velocity
        elif self.type == 'quantum_time_slow':
            # Slow down bird velocity and cap between -10 and 10
            bird.velocity = np.clip(bird.velocity * 0.5, -10, 10)
            return bird.velocity
        elif self.type == 'quantum_shield':
            # Remove all obstacles on screen (shield effect)
            for obstacle in obstacles:
                obstacle.height = 0
            bird.apply_power_up("shield")
            return bird.velocity
        else:
            # Default case: no effect
            return bird.velocity
