# modules/bird.py

import pygame
import numpy as np
from modules.settings import *  # Import all necessary settings
import logging
import random

class Bird:
    """
    Represents the player's bird character in the game.
    Handles movement, rendering, and special abilities.
    """

    def __init__(self):
        """Initializes the bird with default properties."""
        # Load bird animation frames
        try:
            self.images = [pygame.image.load(frame).convert_alpha() for frame in BIRD_FRAMES]
            logging.info("Bird animation frames loaded successfully.")
        except pygame.error as e:
            logging.error(f"Error loading bird frames: {e}")
            self.images = [pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT)) for _ in BIRD_FRAMES]
            for img in self.images:
                img.fill(BIRD_COLOR)

        self.current_frame = 0
        self.animation_speed = ANIMATION_SPEED
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = BIRD_START_X
        self.rect.y = BIRD_START_Y

        # Movement properties
        self.velocity = 0.0
        self.acceleration = GRAVITY
        self.air_resistance = AIR_RESISTANCE
        self.max_velocity = MAX_VELOCITY
        self.min_velocity = MIN_VELOCITY
        self.rotation_angle = 0
        self.is_flapping = False
        self.flap_cooldown = 0
        self.flap_cooldown_time = FLAP_COOLDOWN_TIME

        # Abilities and power-ups
        self.shield_active = False
        self.shield_duration = 0
        self.laser_cooldown = LASER_COOLDOWN_TIME
        self.lightsaber_active = False
        self.lightsaber_color = LASER_COLOR
        self.lightsaber_length = LIGHTSABER_LENGTH
        self.pulse_offset = 0  # Initialize pulse_offset for shield effect

        # Visual properties
        self.color = BIRD_COLOR

        # Quantum mechanics placeholders
        self.superposition_active = False
        self.entanglement_linked = False

    def update_with_dt(self, dt):
        """
        Updates the bird's position, velocity, and handles animations based on delta time.
        Should be called every frame.
        """
        if not self.is_flapping:  # Apply gravity only when not flapping
            self.velocity += self.acceleration * dt

        self.velocity *= self.air_resistance
        self.velocity = max(min(self.velocity, self.max_velocity), self.min_velocity)
        self.rect.y += self.velocity * dt

        # Rotate bird based on velocity
        self.rotation_angle = max(-BIRD_ROTATION_LIMIT, min(self.velocity * ROTATION_SCALING, BIRD_ROTATION_LIMIT))
        rotated_image = pygame.transform.rotate(self.images[int(self.current_frame)], self.rotation_angle)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.rect.center)

        # Update animation frame based on animation speed
        self.current_frame += self.animation_speed * dt
        if self.current_frame >= len(self.images):
            self.current_frame = 0

        # Flap cooldown
        if self.flap_cooldown > 0:
            self.flap_cooldown -= 1
            if self.flap_cooldown <= 0:
                self.is_flapping = False

        # Update shield pulse effect
        if self.shield_active:
            self.pulse_offset += 2  # Adjust pulse speed as needed

        # Keep bird within screen bounds
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))  # Use HEIGHT instead of WINDOW_HEIGHT
        if self.rect.y == 0:
            self.velocity = max(self.velocity, 0)
        elif self.rect.y == HEIGHT - self.rect.height:
            self.velocity = 0

    def flap(self):
        """
        Makes the bird flap, giving it an upward velocity boost.
        """
        if self.flap_cooldown <= 0:
            self.velocity = FLAP_STRENGTH
            self.is_flapping = True
            self.flap_cooldown = self.flap_cooldown_time
            logging.debug("Bird flapped.")

    def draw(self, screen):
        """
        Draws the bird on the screen.
        If the shield or lightsaber is active, draws them as well.
        """
        if self.shield_active:
            pulse_color = (
                self.color[0],
                (self.color[1] + self.pulse_offset) % 255,
                (self.color[2] + self.pulse_offset) % 255
            )
        else:
            pulse_color = self.color

        tinted_image = self.image.copy()
        tinted_image.fill(pulse_color, special_flags=pygame.BLEND_MULT)
        screen.blit(tinted_image, self.rect)

        # Draw shield
        if self.shield_active:
            self.draw_shield(screen)

        # Draw lightsaber
        if self.lightsaber_active:
            self.draw_lightsaber(screen)

    def draw_shield(self, screen):
        """
        Draws a pulsing shield around the bird.
        """
        shield_radius = self.rect.width + 10 + (self.pulse_offset % 10)
        shield_rect = self.rect.inflate(shield_radius, shield_radius)
        shield_color = tuple(
            min(255, c + self.pulse_offset % 100) for c in SHIELD_COLOR
        )
        pygame.draw.ellipse(screen, shield_color, shield_rect, 2)

    def draw_lightsaber(self, screen):
        """
        Draws a lightsaber extending from the bird.
        """
        start_pos = (self.rect.centerx, self.rect.centery)
        angle_rad = -self.rotation_angle * (np.pi / 180)
        end_pos = (
            start_pos[0] + self.lightsaber_length * np.cos(angle_rad),
            start_pos[1] + self.lightsaber_length * np.sin(angle_rad),
        )
        pygame.draw.line(screen, self.lightsaber_color, start_pos, end_pos, 5)

    def activate_lightsaber(self):
        """Activates the bird's lightsaber."""
        self.lightsaber_active = True
        logging.info("Lightsaber activated.")

    def deactivate_lightsaber(self):
        """Deactivates the bird's lightsaber."""
        self.lightsaber_active = False
        logging.info("Lightsaber deactivated.")

    def apply_power_up(self, power_up_type):
        """
        Applies a power-up effect to the bird.

        Args:
            power_up_type (str): The type of power-up to apply.
        """
        if power_up_type == "shrink":
            new_width = int(self.rect.width * SHRINK_SCALE)
            new_height = int(self.rect.height * SHRINK_SCALE)
            self.rect.inflate_ip(-self.rect.width * (1 - SHRINK_SCALE), -self.rect.height * (1 - SHRINK_SCALE))
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
            logging.info("Shrink power-up applied.")
        elif power_up_type == "shield":
            self.shield_active = True
            self.shield_duration = SHIELD_DURATION
            self.pulse_offset = 0  # Reset pulse offset when activating shield
            logging.info("Shield power-up applied.")
        elif power_up_type == "slowdown":
            self.air_resistance = SLOWDOWN_AIR_RESISTANCE
            logging.info("Slowdown power-up applied.")
        elif power_up_type == "score":
            logging.info("Score power-up applied.")
        elif power_up_type == "lightsaber":
            self.activate_lightsaber()
            logging.info("Lightsaber power-up applied.")

    def reset_power_ups(self):
        """Resets all power-up effects."""
        self.air_resistance = AIR_RESISTANCE
        self.shield_active = False
        self.shield_duration = 0
        self.pulse_offset = 0  # Reset pulse offset when deactivating shield
        self.lightsaber_active = False
        self.rect.size = (BIRD_WIDTH, BIRD_HEIGHT)
        self.image = pygame.transform.scale(self.image, (BIRD_WIDTH, BIRD_HEIGHT))
        logging.info("All power-ups reset.")

    def handle_quantum_superposition(self):
        """Handles the bird's behavior while in a superposition state."""
        self.rect.x += random.randint(-2, 2)
        self.rect.y += random.randint(-2, 2)

    def handle_quantum_entanglement(self):
        """Handles the bird's behavior while entangled."""
        pass

    def ai_behavior(self):
        """Placeholder for AI-driven movement or behavior."""
        pass

    def quantum_error_correction(self):
        """Placeholder for quantum error correction algorithms."""
        pass

    def quantum_walk(self):
        """Placeholder for implementing a quantum random walk."""
        pass

    def quantum_optimization(self):
        """Placeholder for implementing quantum optimization algorithms (VQE, QAOA)."""
        pass

    def quantum_circuit_optimization(self):
        """Placeholder for quantum circuit optimization methods."""
        pass

    def get_current_ability(self):
        """Returns the current ability of the bird."""
        if self.lightsaber_active:
            return 'Laser'
        elif self.shield_active:
            return 'Shield'
        else:
            return 'Speed'
