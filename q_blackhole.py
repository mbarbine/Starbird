import pygame
import numpy as np
import random
from settings import *

class QBlackHole:
    def __init__(self, x, speed=PIPE_SPEED):
        self.x = x
        self.radius = BLACK_HOLE_RADIUS
        self.center_y = WINDOW_HEIGHT // 2
        self.speed = speed
        self.color = BLACK_HOLE_COLOR
        self.pulse_offset = 0  # For a pulsing visual effect
        self.pulse_speed = 0.1  # Speed of the pulsing effect
        self.gravity_strength = 5  # Base gravity strength

        # Load sound effect for black hole
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.blackhole_sound = pygame.mixer.Sound('assets/blackhole.wav')
        self.blackhole_sound.set_volume(0.5)  # Adjust the volume as needed
        self.blackhole_sound.play(-1)  # Loop the sound for as long as the black hole exists

        # Adding quantum visual effects
        self.quantum_effect_timer = 0
        self.quantum_effect_frequency = 60  # Quantum effects trigger every second at 60 FPS
        self.quantum_color = (255, 0, 255)  # Quantum glow color
        self.quantum_glow_intensity = 1.0

        # Chaos effect for unpredictable behavior
        self.chaos_active = False
        self.chaos_timer = 0
        self.chaos_duration = random.randint(100, 200)  # Random duration for chaos effect

    def update(self, bird=None):
        """Update black hole position, handle chaos effects, and apply gravity on the bird."""
        self.x -= self.speed
        self.pulse_offset += self.pulse_speed
        self.quantum_effect_timer += 1
        if self.pulse_offset > 2 * np.pi:
            self.pulse_offset = 0

        # Trigger chaos effect randomly
        if not self.chaos_active and random.random() < 0.01:  # 1% chance to trigger chaos
            self.activate_chaos()

        # Handle chaos effect
        if self.chaos_active:
            self.chaos_timer -= 1
            self.apply_chaos_effect()
            if self.chaos_timer <= 0:
                self.chaos_active = False
                self.speed = PIPE_SPEED  # Reset speed after chaos

        # Apply gravity if bird is within range
        if bird:
            self.apply_gravity(bird)

        # Ensure the black hole is within screen bounds
        if self.off_screen():
            self.blackhole_sound.stop()

    def activate_chaos(self):
        """Activate quantum chaos, altering the black hole's properties randomly."""
        self.chaos_active = True
        self.chaos_timer = self.chaos_duration

    def apply_chaos_effect(self):
        """Apply random effects during quantum chaos."""
        if random.random() < 0.1:  # 10% chance to flip direction
            self.speed *= -1
        if random.random() < 0.1:  # 10% chance to change radius
            self.radius = random.randint(10, 40)
        if random.random() < 0.1:  # 10% chance to teleport vertically
            self.center_y = random.randint(50, WINDOW_HEIGHT - 50)
        self.quantum_glow_intensity = 1.5 + 0.5 * np.sin(pygame.time.get_ticks() / 100.0)

    def draw(self, screen):
        # Pulsing effect for the black hole
        pulse_radius = self.radius + int(self.radius * 0.1 * np.sin(self.pulse_offset))
        pygame.draw.circle(screen, self.color, (self.x, self.center_y), pulse_radius)

        # Draw a swirling effect around the black hole
        for i in range(10):
            swirl_radius = int(self.radius * (1 + 0.2 * np.sin(self.pulse_offset + i * np.pi / 5)))
            swirl_color = (self.color[0], max(0, self.color[1] - i * 20), max(0, self.color[2] - i * 20))
            pygame.draw.circle(screen, swirl_color, (self.x, self.center_y), swirl_radius, 1)

        # Quantum effect - a bright flash every quantum_effect_frequency frames
        if self.quantum_effect_timer >= self.quantum_effect_frequency:
            pygame.draw.circle(screen, self.quantum_color, (self.x, self.center_y), pulse_radius + 10, 3)
            self.quantum_effect_timer = 0

        # Draw enhanced glow during chaos
        if self.chaos_active:
            glow_radius = int(pulse_radius * self.quantum_glow_intensity)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, self.quantum_color + (50,), (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, (self.x - glow_radius, self.center_y - glow_radius), special_flags=pygame.BLEND_RGBA_ADD)

    def off_screen(self):
        return self.x < -self.radius

    def collide(self, bird):
        bird_center = bird.rect.center
        distance = np.linalg.norm(np.array([self.x, self.center_y]) - np.array(bird_center))
        if distance < self.radius:
            return True
        return False

    def apply_gravity(self, bird):
        """Apply gravitational pull on the bird."""
        bird_center = bird.rect.center
        direction = np.array([self.x, self.center_y]) - np.array(bird_center)
        distance = np.linalg.norm(direction)
        if distance < self.radius * 5:
            pull_strength = max(1, int(self.gravity_strength * self.radius / (distance ** 1.5)))
            bird.rect.x += int(pull_strength * direction[0] / distance)
            bird.rect.y += int(pull_strength * direction[1] / distance)

            # Rotate the bird slightly as it gets pulled towards the black hole
            bird.rotation_angle += pull_strength

    def hit_by_laser(self, lasers):
        """Black holes are immune to lasers, so always return False."""
        return False

    def __del__(self):
        # Stop the black hole sound when the object is destroyed
        if pygame.mixer.get_init():
            self.blackhole_sound.stop()
